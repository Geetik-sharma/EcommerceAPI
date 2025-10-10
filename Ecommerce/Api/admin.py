from django.contrib import admin
from .models import CustomUser,Product,Category, cart, cart_item
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(cart)
admin.site.register(cart_item)