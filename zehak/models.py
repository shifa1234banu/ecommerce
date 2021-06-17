from django.db import models
from django.contrib.auth.models import User
from week8.models import Product
import random

from django.contrib import messages



# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    num = models.IntegerField()
    
   


    def __str__(self):
        return self.num

    # def save(self, *args, **kwargs):
    #     if self.num is not None:
    #         account_sid ='AC71c08d07ed3583edf7657ecd0040d057'
    #         auth_token = '87ac49a092c370a9f358dbd11d3ed7e3'
    #         client = Client(account_sid, auth_token)

    #         message = client.messages.create(
    #                                     body=f'OTP login - {self.validnum}',
    #                                     from_='+1 781 661 5912',
    #                                     to='+91' +self.num
    #                                     )

    #         print(message.sid)    
    #     return super().save(*args, **kwargs)


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
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
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