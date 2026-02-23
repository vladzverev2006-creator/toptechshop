from django.contrib import admin

from .models import (
    License,
    Product,
    ProductAttribute,
    ProductFile,
    ProductImage,
    ProductVersion,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'price', 'category', 'creator')
    search_fields = ('title', 'description')
    list_filter = ('status', 'category')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductFileInline, ProductAttributeInline]
    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'description', 'status')}),
        ('Цена и лицензия', {'fields': ('price', 'license')}),
        ('Категории', {'fields': ('category', 'tags')}),
        ('Медиа', {'fields': ('cover',)}),
        ('Рейтинг', {'fields': ('rating_avg', 'rating_count')}),
    )
    readonly_fields = ('rating_avg', 'rating_count')


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')
    search_fields = ('title', 'code')


@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version', 'created_at')
    search_fields = ('product__title', 'version')


@admin.register(ProductFile)
class ProductFileAdmin(admin.ModelAdmin):
    list_display = ('product', 'file', 'uploaded_at')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'alt_text')


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')
