from django.contrib import admin
from .models import CustomUser,Product,Category, cart, cart_item, Review, Product_Rating, Wishlist
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(cart)
admin.site.register(cart_item)
admin.site.register(Review)
admin.site.register(Product_Rating)
admin.site.register(Wishlist)