from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .forms import ProfileForm, RegisterForm


MAX_LOGIN_ATTEMPTS = 5
BLOCK_MINUTES = 10


def _login_block_key(ip):
    return f'login_block_{ip}'


def _login_attempt_key(ip):
    return f'login_attempt_{ip}'


def login_view(request):
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    if cache.get(_login_block_key(ip)):
        messages.error(request, 'Слишком много попыток. Попробуйте позже.')
        return render(request, 'accounts/login.html', {'form': AuthenticationForm(request)})

    if request.method == 'POST':
        username = request.POST.get('username', '')
        user_model = get_user_model()
        user_obj = user_model.objects.filter(username=username).first()
        if user_obj and not user_obj.is_active:
            messages.error(request, 'Подтвердите email перед входом.')
            return render(request, 'accounts/login.html', {'form': AuthenticationForm(request)})
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                cache.delete(_login_attempt_key(ip))
                messages.success(request, 'Вы вошли в систему')
                return redirect(request.GET.get('next') or 'core:home')
        attempts = cache.get(_login_attempt_key(ip), 0) + 1
        cache.set(_login_attempt_key(ip), attempts, BLOCK_MINUTES * 60)
        if attempts >= MAX_LOGIN_ATTEMPTS:
            cache.set(_login_block_key(ip), True, BLOCK_MINUTES * 60)
        messages.error(request, 'Неверные данные')
    else:
        form = AuthenticationForm(request)

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = user.userprofile
            profile.email_verified = False
            profile.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activate_url = request.build_absolute_uri(
                reverse('accounts:activate', args=[uid, token])
            )
            subject = 'TopTechShop — подтвердите ваш email'
            message = (
                'Здравствуйте!\n\n'
                'Вы создали аккаунт в TopTechShop. Чтобы завершить регистрацию, '
                'подтвердите email по ссылке ниже:\n'
                f'{activate_url}\n\n'
                'Если это были не вы, просто проигнорируйте это письмо.\n\n'
                'С уважением,\n'
                'Команда TopTechShop'
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            return render(request, 'accounts/verify_notice.html', {'email': user.email})
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('core:home')


@login_required
def profile_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


def activate_view(request, uidb64, token):
    user_model = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user_model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        profile = user.userprofile
        profile.email_verified = True
        profile.save()
        messages.success(request, 'Email подтверждён. Теперь можно войти.')
        return redirect('accounts:login')
    messages.error(request, 'Ссылка подтверждения недействительна или устарела.')
    return redirect('accounts:register')


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    email_template_name='accounts/password_reset_email.html',
                    subject_template_name='accounts/password_reset_subject.txt',
                )
                messages.success(request, 'Инструкция по восстановлению отправлена.')
                return redirect('accounts:password_reset_done')
            except Exception:
                messages.error(request, 'Не удалось отправить письмо. Попробуйте позже.')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})
