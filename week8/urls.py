from django.urls import path
from . import views


urlpatterns =[
    path('',views.login,name='adlogin'),
    path('ad_home',views.ad_home,name='ad_home'),
    path('user',views.user,name='user'),
    path('ad_logout',views.ad_logout,name='ad_logout'),
    path('logincheck',views.logincheck,name='logincheck'),
    path('product',views.product,name='product'),
    path('add_product',views.add_product,name='add_product'),
    path('addsize',views.addsize,name='addsize'),
    path('edit_product/<id>',views.edit_product,name='edit_product'),
    path('delete_product/<id>',views.delete_product,name='delete_product'),
    path('delete_check/<id>',views.delete_check,name='delete_check'),
    path('category',views.category,name='category'),
    path('delete_category/<id>',views.delete_category,name='delete_category'),
    path('edit_category/<id>',views.edit_category,name='edit_category'),
    path('category_check/<id>',views.category_check,name='category_check'),
    path('add_category',views.add_category,name='add_category'),
    path('block_user/<id>',views.block_user,name='block_user'),
    path('unblock_user/<id>',views.unblock_user,name='unblock_user'),
    path('order',views.order,name='order'),
    path('admin_order_status/',views.admin_order_status,name='admin_order_status'),
    path('coupon',views.coupon,name='coupon'),
    path('category_offer/<id>',views.category_offer,name='category_offer'),
    path('sale',views.sale,name='sale'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
   
]