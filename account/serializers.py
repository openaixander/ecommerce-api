from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VendorProfile

User = get_user_model()


class RegistrationSerialzer(serializers.ModelSerializer):
    # write only, it goes in but never comes out
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'is_vendor',
            'is_customer'
            ]
        
    # we then override the create method because standard serializers don't hash passwords.
    # They just save raw text. We need to use 'create_user'.

    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_vendor=validated_data.get('is_vendor',False),
            is_customer=validated_data.get('is_customer',True)
        )

        return user

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = [
            'store_name',
            'store_description',
            'store_logo'
            ]
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_vendor', 'is_customer']