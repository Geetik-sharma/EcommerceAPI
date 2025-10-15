from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

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
        return f"{self.quantity} X {self.product} in cart {self.cart.cart_id}"

class Review(models.Model):
    rating_choices=[
        (1,"Poor"),
        (2,"Fair"),
        (3,"Good"),
        (4,"Very Good"),
        (5, "Excellent")
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating=models.PositiveIntegerField(choices=rating_choices)
    review=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s review on {self.product.name}"
    class Meta:
        unique_together=["user","product"]
        ordering=["-created_on"]

class Product_Rating(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE,related_name="rating")
    average_rating=models.FloatField(default=0.0)
    total_ratings=models.PositiveBigIntegerField(default=0.0)

    def __str__(self):
        return f"{self.product.name} - {self.average_rating} ({self.total_ratings} ratings)"