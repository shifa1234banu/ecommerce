from django.urls import path
from . import views


urlpatterns =[
    path('',views.login,name='login'),
    path('adhome',views.adhome,name='adhome'),
    path('user',views.user,name='user'),
    path('logout',views.logout,name='logout'),

    path('product',views.product,name='product'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('addsize',views.addsize,name='addsize'),
    path('editproduct/<id>',views.editproduct,name='editproduct'),
    path('deleteproduct/<id>',views.deleteproduct,name='deleteproduct'),
    path('deletecheck/<id>',views.deletecheck,name='deletecheck'),
    path('category',views.category,name='category'),
    path('deletecategory/<id>',views.deletecategory,name='deletecategory'),
    path('categorycheck/<id>',views.categorycheck,name='categorycheck'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('blockuser/<id>',views.blockuser,name='blockuser'),
    path('unblockuser/<id>',views.unblockuser,name='unblockuser'),
   
]