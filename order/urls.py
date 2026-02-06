from django.urls import path
from . import views



urlpatterns = [
    path('cart/', views.my_cart, name='my-cart'),
    path('cart/add/', views.add_to_cart, name='add-to-cart'),
    path('checkout/', views.checkout, name='checkout'),

    # vendor dashboard
    path('vendor/orders/', views.vendor_orders, name='vendor-orders'),
]