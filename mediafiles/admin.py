from django.contrib import admin

from .models import Download


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'file', 'downloaded_at')
    search_fields = ('user__username', 'product__title')
