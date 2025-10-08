from rest_framework import serializers
from .models import Product, CustomUser, Category

class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Product
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