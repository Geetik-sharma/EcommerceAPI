from rest_framework import serializers
from .models import Product, CustomUser, Category, cart, cart_item, Review, Wishlist
from django.contrib.auth import get_user_model

class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class Category_Detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class Category_Serializer(serializers.ModelSerializer):
    Products=Product_Serializer(many=True, read_only=True)
    class Meta:
        model=Category
        fields="__all__"

class Product_Detail_serializer (serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
  
class Cart_Item_Serializer(serializers.ModelSerializer):
    product=Product_Detail_serializer(read_only=True)
    subtotal=serializers.SerializerMethodField()
    class Meta:
        model=cart_item
        fields=["id", "product", "quantity", "subtotal"]
    def get_subtotal(self,cart_item):
        total=cart_item.quantity * cart_item.product.price
        return total

class CartSerializer(serializers.ModelSerializer):
    cart_items=Cart_Item_Serializer(many=True, read_only=True)
    cart_total=serializers.SerializerMethodField()
    class Meta:
        model=cart
        fields=["id","cart_id","cart_items","cart_total"]
    def get_cart_total(self,cart):
        items=cart.cart_items.all()
        total=0
        for items in items:
            total+=items.quantity * items.product.price
        return total
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=['id','first_name','last_name','profile_picture_url']

class Review_Serializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Review
        fields=['id','user','rating','review','created_on','updated_on']

class Wishlist_Serializer(serializers.ModelSerializer):

    class Meta:
        model=Wishlist
        fields=["id","user","product","created_on"]