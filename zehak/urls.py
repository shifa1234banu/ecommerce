from django.urls import path
from . import views


urlpatterns =[
    path('',views.home,name='home'),
    
    path('register',views.register,name='register'),
    path('verify',views.verify,name='verify'),
    path('size',views.size,name='size'),
    path('otplogin',views.otplogin,name='otplogin'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('logout',views.logout,name='logout'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('logincheck',views.logincheck,name='logincheck'),
    path('cart',views.cart,name='cart'),
    path('add_cart/',views.add_cart,name='add_cart'),
    path('remove_cart/',views.remove_cart,name='remove_cart'),
    path('update_cart/',views.update_cart,name='update_cart'),
    path('remove_cart_item/<id>/',views.remove_cart_item,name='remove_cart_item'),
    path('checkout',views.checkout,name='checkout'),
    path('productdetails/<id>/',views.productdetails,name='productdetails'),
    path('search',views.search,name='search'),
    path('address',views.address,name='address'),
    path('otp',views.otp,name='otp'),
    path('myorder',views.myorder,name='myorder'),
    path('paypal/',views.paypal,name='paypal'),
    path('place_order',views.place_order,name='place_order'),
    # path('razorpay1',views.razorpay1,name='razorpay1'),
    path('razorsuccess',views.razorsuccess,name='razorsuccess'),
    path('catformal/<id>',views.catformal,name='catformal'),
    path('brand/<bar>',views.brand,name='brand'),
    path('delete_order/<id>',views.delete_order,name='delete_order'),

    #########coupon
    path('couponcheck',views.couponcheck,name='couponcheck'),

    
]