from django.shortcuts import render
from .Serializers import Product_Serializer, Category_Serializer, Product_Detail_serializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins,generics,viewsets
from .models import Product,Category
from rest_framework import status
from django.http import Http404
# Create your views here.

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
    def check (self,pk):
        try:
            return Product.objects.all(pk=pk)
        except Product.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        prod=Product.objects.get(pk=pk)
        serializer=Product_Serializer(prod)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    def put (self,request,pk):
        serializer=Product_Serializer(Product.objects.get(pk=pk),data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        self.check(pk).delete()
        return Response (status=status.HTTP_404_NOT_FOUND)
