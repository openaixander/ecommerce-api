from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
# Create your models here.


User = get_user_model()


class Order(models.Model):
    # we will rename 'cart' to 'order' for it is better

    ORDERSTATUS = (
        ('cart','Cart'),
        ('paid','Paid'),
        ('shipped','Shipped'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDERSTATUS, default='cart')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

