from django.contrib import admin


from .models import OrderItem
# Register your models here.


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('')

admin.site.register(OrderItem)