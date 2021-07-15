from django.db import models
from django.contrib.auth.models import User
from week8.models import Product
import random
import uuid
from django.contrib import messages



# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    num = models.CharField(max_length=15)
    
    userimage = models.ImageField(null=True,blank=True,upload_to='photos/productimages',default='user/images/user.png')
    
   


    def __str__(self):
        return str(self.num)

   


    def checkotp(self,otp):
        if str(self.vnum) ==otp:
            return True
        else:
            return False        


    
class Cart(models.Model):
    
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    


class CartItem(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.product.price * self.quantity
    
    
    
    
    
    def __str__(self):
        return self.product

class Address(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,blank=True)
    email = models.EmailField(max_length=70,blank=True)
    address1 = models.CharField(max_length=250,blank=True)
    address2 = models.CharField(max_length=250)
    mobilenumber = models.IntegerField(blank=True)
    post = models.IntegerField(blank=True)
    landmark = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)

    
    def __str__(self):
        return self.first_name




Variation_category_choice = (
    ('size','size'),
)        



class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Variation_category = models.CharField(max_length=100,choices=Variation_category_choice)
    Variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
  

    def __str__(self):
        return self.product




  



class Order(models.Model):
    STATUS = {
        ('Placed','Placed'),
        ('Cancelled','Cancelled'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Returned','Returned')                                                                 
    }                                               
    PAYMENT_STATUS = {                                                                                  
        ('Success','Success'),
        ('Failed','Failed'),
        ('Pending','Pending'),
    }

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    price = models.IntegerField()
    address = models.ForeignKey(Address,on_delete=models.CASCADE,null=True)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS,default='Placed')
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default='Success')
    pay_method = models.CharField(max_length=100,default=100)
    


    def __str__(self):
        return self.item 




