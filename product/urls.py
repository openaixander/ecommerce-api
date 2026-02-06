from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),
    # Always put specific paths (create/) BEFORE dynamic paths (<slug>/)
    path('products/<slug:slug>/', views.product_detail, name='product-detail'),
]