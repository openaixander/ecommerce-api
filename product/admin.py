from django.contrib import admin
from .models import Category, Product, ProductImage

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {
        'slug': ('title',)
        }

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {
        'slug': ('title',)
        }

admin.site.register(Category, CategoryAdmin)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)