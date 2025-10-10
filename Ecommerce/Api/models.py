from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    profile_picture_url=models.URLField(blank=True,null=True)
    def __str__(self):
        return self.email

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField()
    category_image=models.ImageField(upload_to='products_img',blank=True,null=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='products_img',blank=True,null=True)
    featured=models.BooleanField(default=True)
    slug=models.SlugField(unique=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True,related_name='Products')
    def __str__(self):
        return self.name

class cart(models.Model):
    cart_id=models.CharField(max_length=11,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.cart_id


class cart_item(models.Model):
    cart=models.ForeignKey(cart,on_delete=models.CASCADE,related_name="cart_items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="products")
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quentity} X {self.product} in cart {self.cart.cart_id}"
