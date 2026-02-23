from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from accounts.models import Role
from categories.models import Category, Tag
from products.models import License, Product


class Command(BaseCommand):
    help = 'Seed demo data'

    def handle(self, *args, **options):
        role_user, _ = Role.objects.get_or_create(code='user', title='User')
        role_seller, _ = Role.objects.get_or_create(code='seller', title='Seller')
        role_staff, _ = Role.objects.get_or_create(code='staff', title='Staff')

        Group.objects.get_or_create(name='seller')

        if not User.objects.filter(username='demo').exists():
            user = User.objects.create_user(username='demo', password='demo12345', email='demo@toptechshop.isgood.host')
            user.userprofile.role = role_user
            user.userprofile.save()

        cat_ui, _ = Category.objects.get_or_create(name='UI‑киты', description='Дизайн системы')
        cat_tpl, _ = Category.objects.get_or_create(name='Шаблоны', description='Готовые шаблоны')
        Tag.objects.get_or_create(name='Figma')
        Tag.objects.get_or_create(name='SaaS')

        license_std, _ = License.objects.get_or_create(code='standard', title='Standard', terms='Лицензия для 1 проекта')

        if not Product.objects.exists():
            Product.objects.create(
                title='SaaS UI‑kit 2026',
                description='Набор экранов и компонентов',
                price=12000,
                status='active',
                creator=User.objects.first(),
                category=cat_ui,
                license=license_std,
            )
            Product.objects.create(
                title='Fintech Landing Pack',
                description='Готовые лендинги',
                price=8500,
                status='active',
                creator=User.objects.first(),
                category=cat_tpl,
                license=license_std,
            )

        self.stdout.write(self.style.SUCCESS('Demo data created'))
