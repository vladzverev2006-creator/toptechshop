from django.conf import settings
from django.db import models

from products.models import Product, ProductFile


class Download(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='downloads')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ForeignKey(ProductFile, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-downloaded_at']

    def __str__(self):
        return f'{self.user.username} -> {self.product.title}'

# Create your models here.
