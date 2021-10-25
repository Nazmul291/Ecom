from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.search, name="search"),
    path('product_details/<int:product_id>', views.product_details, name="product_details"),
    path('check_item', views.check_item, name="check_item"),
    path('register', views.user_registration, name="user_registration"),
    path('login', views.user_login, name="user_login"),
    path('logout', views.user_logout, name="user_logout"),
    path('addcart', views.addcart, name="addcart"),
    path('remove_cart', views.remove_cart, name="remove_cart"),
    path('btn_plus', views.btn_plus, name="btn_plus"),
    path('btn_minus', views.btn_minus, name="btn_minus"),
    path('cupon', views.cupon, name="cupon"),
]
