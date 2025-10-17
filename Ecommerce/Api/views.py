from django.shortcuts import render
from .Serializers import Product_Serializer, Category_Serializer, Product_Detail_serializer,Category_Detail_Serializer,CartSerializer, Cart_Item_Serializer,Review_Serializer, Wishlist_Serializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins,generics,viewsets
from rest_framework.decorators import api_view
from .models import Product,Category,cart,cart_item,Review,Wishlist
from rest_framework import status
from django.http import Http404
from django.contrib.auth import get_user_model
from django.db.models import Q

User=get_user_model()
# Create your views here.

class categorys(APIView):
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
    def put(self,request,pk):
        quantity=int(request.data.get("quantity"))

        cartitem=cart_item.objects.get(id=pk)
        cartitem.quantity=quantity
        cartitem.save()

        serializer=Cart_Item_Serializer(cartitem)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class Cart_item_delete(APIView):
    def delete(self, request, pk):
        cart_item.objects.get(id=pk).delete()
        return Response (status=status.HTTP_204_NO_CONTENT)

class addreview(APIView):
    def post(self,request):
        product_id=request.data.get("product_id")
        email_id=request.data.get("email_id")
        rating=request.data.get("rating")
        review_text=request.data.get("review")
        print(product_id,email_id ,rating,review_text)

        product=Product.objects.get(id=product_id)
        user, created=User.objects.get_or_create(email=email_id, defaults={"username":email_id.split("@")[0]})
        

        review=Review.objects.create(product=product, user=user, rating=rating, review=review_text)
        serializer=Review_Serializer(review)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class Update_review(APIView):
    def check(self,pk):
        try:
            return Review.objects.get(id=pk)
        except Review.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        serializer=Review_Serializer(self.check(pk))
        return Response(serializer.data,status=status.HTTP_302_FOUND)
    def put(self,request,pk):
        review=self.check(pk)
        new_review=request.data.get("review") or request.query_params.get("review")
        new_rating=request.data.get("rating") or request.query_params.get("rating")

        review.review=new_review
        review.rating=new_rating
        review.save()
        serializer=Review_Serializer(review)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self,request,pk):
        self.check(pk).delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class add_wishlist(APIView):
    def post(self,request):
        email=request.data.get("email")
        product_id=request.data.get("product_id")

        user=User.objects.get(email=email)
        product=Product.objects.get(id=product_id)

        wishlist=Wishlist.objects.filter(user=user, product=product)
        if(wishlist):
            wishlist.delete()
            return Response("deleted succesfully",status=status.HTTP_204_NO_CONTENT)
        new_wishlist=Wishlist.objects.create(user=user, product=product)
        new_wishlist.save()
        serializer=Wishlist_Serializer(new_wishlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Search_product(APIView):
    def get(self,request):
        query=request.query_params.get("query")
        print (query)
        if not query:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        prod = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query))
        print(prod)
        serializer=Product_Serializer(prod,many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)
