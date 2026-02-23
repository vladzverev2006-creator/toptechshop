from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


class Role(models.Model):
    code = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=80)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
    )
    bio = models.TextField(blank=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return self.user.username

# Create your models here.
