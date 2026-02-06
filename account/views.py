from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import VendorProfileSerializer
# Create your views here.



from .serializers import RegistrationSerialzer


@api_view(['POST'])
def register_user(request):
    """Endpoint for a new user to sign up"""

    serializer = RegistrationSerialzer(data=request.data)

    # check whether it is valid
    if serializer.is_valid():
        # save the serializer

        user = serializer.save()


        return Response({
            "message": "User created successfully", 
            "user_id": user.id,
            "email": user.email
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vendor_profile(request):
    """This allows user to have a vendor profile(basically a shop)"""
    user = request.user

    # check for duplicates
    if hasattr(user, 'vendor_profile'):
        return Response(
            {"error": "You already have a vendor profile."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Translate data
    serializer = VendorProfileSerializer(data=request.data)

    # check whether it is valid
    if serializer.is_valid():
        # Inject the user(connect the shop to the owner)
        serializer.save(user=user)

        # auto promote User
        # if there weren't vendor, they are now
        if not user.is_vendor:
            user.is_vendor = True
            user.save()

        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )