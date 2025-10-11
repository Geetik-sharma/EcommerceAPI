from django.shortcuts import render
from .Serializers import Product_Serializer, Category_Serializer, Product_Detail_serializer,Category_Detail_Serializer,CartSerializer, Cart_Item_Serializer,Review_Serializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins,generics,viewsets
from rest_framework.decorators import api_view
from .models import Product,Category,cart,cart_item,Review
from rest_framework import status
from django.http import Http404
from django.contrib.auth import get_user_model

User=get_user_model()
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

class Cart_detail(APIView):
    def post(self,request):
        cart_id=request.query_params.get("cart_id") or request.data.get("cart_id")
        product_id=request.query_params.get("product_id") or request.data.get("product_id")
        print(cart_id,product_id)
        Cart_obj, created=cart.objects.get_or_create(cart_id=cart_id)
        product=Product.objects.get(id=product_id)

        Cartitem, created=cart_item.objects.get_or_create(product=product, cart=Cart_obj)
        Cartitem.quantity=1
        Cartitem.save()

        serializer=CartSerializer(Cart_obj)
        return Response(serializer.data, status=status.HTTP_302_FOUND)

class Update_cartitem_Quantity(APIView):
    def put(self,request):
        cartitem_id=request.data.get("cartitem_id")
        quantity=int(request.data.get("quantity"))

        cartitem=cart_item.objects.get(id=cartitem_id)
        cartitem.quantity=quantity
        cartitem.save()

        serializer=Cart_Item_Serializer(cartitem)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class addreview(APIView):
    def post(self,request):
        product_id=request.data.get("product_id")
        email=request.data.get("email_id")
        rating=request.data.get("rating")
        review_text=request.data.get("review")

        product=Product.objects.get(id=product_id)
        user=User.objects.get(email=email)

        review=Review.objects.create(product=product, user=user, rating=rating, review=review_text)
        serializer=Review_Serializer(review)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
