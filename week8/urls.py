from django.urls import path
from . import views


urlpatterns =[
    path('',views.login,name='adlogin'),
    path('adhome',views.adhome,name='adhome'),
    path('user',views.user,name='user'),
    path('ad_logout',views.ad_logout,name='ad_logout'),
    path('logincheck',views.logincheck,name='logincheck'),
    # path('login',views.login,name='login'),
    path('product',views.product,name='product'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('addsize',views.addsize,name='addsize'),
    path('editproduct/<id>',views.editproduct,name='editproduct'),
    path('deleteproduct/<id>',views.deleteproduct,name='deleteproduct'),
    path('deletecheck/<id>',views.deletecheck,name='deletecheck'),
    path('category',views.category,name='category'),
    path('deletecategory/<id>',views.deletecategory,name='deletecategory'),
    path('editcategory/<id>',views.editcategory,name='editcategory'),
    path('categorycheck/<id>',views.categorycheck,name='categorycheck'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('blockuser/<id>',views.blockuser,name='blockuser'),
    path('unblockuser/<id>',views.unblockuser,name='unblockuser'),
    path('order',views.order,name='order'),
   
    path('admin_order_status/',views.admin_order_status,name='admin_order_status'),
    path('coupon',views.coupon,name='coupon'),
    path('category_offer/<id>',views.category_offer,name='category_offer'),
    path('sale',views.sale,name='sale'),

    
    path('add_coupon',views.add_coupon,name='add_coupon'),
   
]