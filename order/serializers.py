from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer





class OrderItemSerializer(serializers.ModelSerializer):
    # nested serializers (this shows name of prduct, price and image)

    product = ProductSerializer(read_only=True)

    order_id = serializers.ReadOnlyField(source='order.id')
    customer_email = serializers.ReadOnlyField(source='order.user.email')
    created_at = serializers.ReadOnlyField(source='order.created_at')


    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity', 'order_id', 'customer_email', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    # show all items inside this order
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'items', 'created_at']