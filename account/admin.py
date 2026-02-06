from django.contrib import admin
from .models import User, VendorProfile


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'is_vendor',
        'is_customer',
        )

    ordering = ('email',)


@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'store_name',
        'user',
        'created_at',
        )
