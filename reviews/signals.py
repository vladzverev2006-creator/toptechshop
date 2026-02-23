from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count

from .models import Review


@receiver([post_save, post_delete], sender=Review)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    agg = product.reviews.aggregate(avg=Avg('rating'), count=Count('id'))
    product.rating_avg = agg['avg'] or 0
    product.rating_count = agg['count'] or 0
    product.save(update_fields=['rating_avg', 'rating_count'])
