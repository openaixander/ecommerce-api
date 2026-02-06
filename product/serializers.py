from rest_framework import serializers
from .models import Category, Product, ProductImage



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    
class ProductSerializer(serializers.ModelSerializer):
    # nested serializer
    # instead of showing image IDs,

    images = ProductImageSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = [
            "id", 
            "title", 
            "slug", 
            "description", 
            "price", 
            "image", # Main thumbnail
            "images", # The Gallery (Nested)
            "category", 
            "vendor"
        ]
        
        read_only_fields= ['slug', 'vendor']
    


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "slug",
            ]