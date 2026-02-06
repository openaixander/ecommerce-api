from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _




from .managers import CustomUserManager
# Create your models here.


class User(AbstractUser, PermissionsMixin):
    # remove the username field (optional, but cleaner)
    username = None


    # try to make email unique and mandatory
    email = models.EmailField(_('email address'), unique=True)
    
    
    #Roles(whether a vendor or a customer) 
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)



    # this is what makes users sign in with them emails
    USERNAME_FIELD = 'email'

    # these are asked when user is creating a superuser account
    REQUIRED_FIELDS = []


    objects = CustomUserManager()


    def __str__(self):
        return self.email
    

class VendorProfile(models.Model):
    # oTo: One user =  One vendor profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')

    store_name = models.CharField(max_length=100)
    store_description = models.TextField()


    # using 'upload_to' orginizes files
    store_logo = models.ImageField(upload_to='vendors', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name