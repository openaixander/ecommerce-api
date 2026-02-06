from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F

from .models import Order, OrderItem
from product.models import Product
from .serializers import OrderSerializer, OrderItemSerializer


# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    # get the data from the user (Product ID and quantity)

    product_id = request.data.get('product_id')
    print(product_id)
    quantity = int(request.data.get('quantity', 1)) #Default to one if missing

    # get the actual object
    product = get_object_or_404(Product, id=product_id)

    print(f"Product -{product}")

    # GET OR CREATE THE CART(ORDER)
    # find an order for this user with status='cart'
    # if none exists, create a new one

    order, created = Order.objects.get_or_create(
        user=request.user,
        status='cart'
    )


    # CHECK IF ITEM EXISTS in the cart
    # look for an item in this order with this specific product
    item, item_created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'price':product.price, 'quantity': quantity}

    )

    # If it already existed, just update the quantity
    if not item_created:
        item.quantity += quantity
        item.save()
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_cart(request):
    # Find the active cart for this user
    # we use first() instead of get() which returns None if there is no cart available

    order = Order.objects.filter(user=request.user, status='cart').first()


    # what if they have not started shopping yet?
    if not order:
        return Response({'items':[]}, status=status.HTTP_200_OK)

    # translate to JSON
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    # find the open cart
    order = Order.objects.filter(user=request.user, status='cart').first()

    if not order:
        return Response(
            {'error': "No active cart found."}, status=status.HTTP_400_BAD_REQUEST
        )

    # calculate the total price
    # we loop through the items in order

    # total = 0
    # for item in order.items.all():
    #     total += item.price * item.quantity
    total = order.items.aggregate(
        total_cost=Sum(F('price') * F('quantity'))
    )['total_cost']
    # save the total
    order.total_amount = total

    # 4. "Charge the Card" (Simulated)
    # In a real app, here we would talk to Paystack/Stripe API.
    # If Paystack says "Success", THEN we move to step 5.


    # mark as paid
    order.status = 'paid'
    order.save()

    # return the receipt
    serializer = OrderSerializer(order)
    return Response({
        "message": "Payment Successful",
        "order_id": order.id,
        "total_paid": total,
        "data": serializer.data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_orders(request):
    user = request.user

    # check if user a vendor

    if not hasattr(user, 'vendor_profile'):
        return Response(
            {"error": "You are not a vendor"}, status=403
        )
    
    # we want orderitems
    items = OrderItem.objects.filter(
        product__vendor__user=user,
        order__status='paid' #just show items that have been paid for
    ).order_by('-id')


    serializer = OrderItemSerializer(items, many=True)
    return Response(serializer.data)
