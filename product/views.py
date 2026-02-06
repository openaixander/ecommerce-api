from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer

# Create your views here.


# 1. List all Products (Public)
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()

    # let's check if the user sent a search=something in the url
    query = request.GET.get('search')

    if query:
        # filter where title contains query or description contains query
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    # CATEGORY FILTER LOGIC
    category_id = request.GET.get('category_id')

    if category_id:
        products = products.filter(category_id=category_id)

    paginator = PageNumberPagination()
    paginator.page_size = 10

    result_page = paginator.paginate_queryset(products, request)

    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# 2. Product Detail (Public)
@api_view(['GET'])
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


# Look how clean this is.
# We don't write "if request.method == POST". 
# We don't write "serializer.save()".
# We just tell it WHAT to use.

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer # <--- This tells the UI to draw the form!
    permission_classes = [IsAuthenticated]

    # We still need to inject the vendor, so we override this one small method
    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'vendor_profile'):
             # If you want to raise an error here, you can, 
             # but usually permissions handle access.
             raise serializer.ValidationError("You must be a Vendor to create products.")
        
        serializer.save(vendor=user.vendor_profile)