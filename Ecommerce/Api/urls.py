from django.urls import path,include
from .import views
urlpatterns=[
    path("category_list/" ,views.category.as_view() ),
    path("category_detail/<slug:slug>/",views.category_detail.as_view()),
    path("product_list/",views.product.as_view()),
    path("product_detail/<slug:slug>/",views.product_detail.as_view())
]