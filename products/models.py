from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.utils.text import slugify

from categories.models import Category, Tag


def validate_file_size(file):
    max_size_mb = 50
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Файл больше {max_size_mb} MB')


class License(models.Model):
    code = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=120)
    terms = models.TextField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('active', 'Активен'),
        ('archived', 'Архив'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    license = models.ForeignKey(License, on_delete=models.PROTECT)
    cover = models.ImageField(upload_to='products/covers/', blank=True, null=True)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.price < 0:
            raise ValidationError('Цена не может быть отрицательной')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    alt_text = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f'Image for {self.product.title}'


class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='products/files/', validators=[validate_file_size])
    file_type = models.CharField(max_length=60, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'File for {self.product.title}'


class ProductVersion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions')
    version = models.CharField(max_length=40)
    changelog = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'version')

    def __str__(self):
        return f'{self.product.title} v{self.version}'


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField(max_length=80)
    value = models.CharField(max_length=200)

    class Meta:
        unique_together = ('product', 'key')

    def __str__(self):
        return f'{self.key}: {self.value}'

# Create your models here.
