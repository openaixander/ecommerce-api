from django.db import models
from account.models  import VendorProfile
from django.utils.text import slugify
# Create your models here.

# we need three tables in products
# category
# product
# ProductImage



class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    ordering = models.IntegerField(default=0)

    # self-referencing ForeignKey
    # This allows: "Electronics"(parent) -> "Laptops" (Child)

    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # if slug is empty, create one from the title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Product(models.Model):
    # The owner
    vendor = models.ForeignKey(
        VendorProfile,
        related_name='products',
        on_delete=models.CASCADE
        )
    
    # organization
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
        )
    
    # product details
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)


    # 4. The Money (CRITICAL: Use DecimalField)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)


    image = models.ImageField(upload_to='uploads/', blank=True, null=True)


    class Meta:
        # sort by newest
        ordering = ('-date_added',)

    def save(self, *args, **kwargs):
        # if slug is empty, create one from the title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.title
    

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
        )
    
    image = models.ImageField(
        upload_to='upload/products/'
    )

    def __str__(self):
        return f"Image for {self.product.title}"