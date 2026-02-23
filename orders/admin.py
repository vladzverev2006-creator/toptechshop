from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('status',)
    inlines = [OrderItemInline]
    actions = ['mark_completed']

    def mark_completed(self, request, queryset):
        queryset.update(status='completed')

    mark_completed.short_description = 'Отметить как завершённые'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity')
