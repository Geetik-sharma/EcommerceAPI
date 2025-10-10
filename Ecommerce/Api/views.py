from django.shortcuts import render
from .Serializers import Product_Serializer, Category_Serializer, Product_Detail_serializer,Category_Detail_Serializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins,generics,viewsets
from .models import Product,Category
from rest_framework import status
from django.http import Http404
# Create your views here.

class category(APIView):
    def get(self,request):
        cat=Category.objects.all()
        serializer=Category_Detail_Serializer(cat,many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    def create(self,request):
        serializer=Category_Detail_Serializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class category_detail(APIView):
    def get(self,request,slug):
        cat=Category.objects.get(slug=slug)
        serializer=Category_Serializer(cat)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
   

class product(APIView):
    def get(self,request):
        prod=Product.objects.filter(featured=True)
        serializer=Product_Serializer(prod,many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    def create(self,request):
        serializer=Product_Serializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class product_detail(APIView):
    def check (self,slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404
    def get(self,request,slug):
        prod=Product.objects.get(slug=slug)
        serializer=Product_Detail_serializer(prod)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    def put (self,request,slug):
        serializer=Product_Detail_serializer(Product.objects.get(slug=slug),data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,slug):
        self.check(slug).delete()
        return Response (status=status.HTTP_404_NOT_FOUND)

