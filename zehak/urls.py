from django.urls import path
from . import views


urlpatterns =[
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
     path('verify',views.verify,name='verify'),
    
    path('otplogin',views.otplogin,name='otplogin'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('logincheck',views.logincheck,name='logincheck'),
    path('cart',views.cart,name='cart'),
    path('add_cart/<id>',views.add_cart,name='add_cart'),
    path('remove_cart/<id>',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<id>',views.remove_cart_item,name='remove_cart_item'),
    path('checkout',views.checkout,name='checkout'),
    path('productdetails/<id>/',views.productdetails,name='productdetails'),
    path('search',views.search,name='search'),
    path('address',views.address,name='address'),

    

    path('otp',views.otp,name='otp'),
    
]