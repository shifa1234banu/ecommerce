from django.shortcuts import render,redirect,get_object_or_404
from week8.models import Product
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Profile,Cart,CartItem,Address
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,Count
from .forms import AddressForm
import random
from twilio.rest import Client
from django.contrib.auth.decorators import login_required



# import os
# import random
# from twilio.rest import Client

# Create your views here.


def home(request):
    queryset = Product.objects.all()
    context = {'products' : queryset}
    return render(request,"user/index.html",context)
       

def userlogin(request):
    return render(request,"user/login.html")


def productdetails(request, id):
    product = Product.objects.get(id=id)
    context={'product' : product}
    return render(request,"user/product-details.html", context)    



def otp(request):
    return render(request,"user/otp.html")    


def register(request):
      
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            num = request.POST['num']
            password = request.POST['password1']
            username = request.POST['username']
            

            check_user = User.objects.filter(email=email).first()
            check_profile = Profile.objects.filter(num=num).first()
            
            if check_user or check_profile :
                context = {'message' : 'user already exist','class' : 'danger'}
                return render(request,"user/login.html",context) 

            user =User.objects.create_user(first_name =first_name,last_name=last_name,email=email,password=password,username=username)
            user.save()

            
            
            
            profile = Profile(user=user,num=num)
            profile.save()
            print('working')
            request.session['validnum'] = 'validnum'
            return redirect('home')

        return render(request,"user/register.html")



def logincheck(request):
    
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request, user)
                request.session['num'] = 'num'
                return redirect('home')
            else:
                messages.info(request, 'invalid credentials')
                return redirect('userlogin')
        else:
            return redirect('userlogin')   

def otplogin(request):
    if request.method == 'POST':
        num = request.POST['num']
        is_user = Profile.objects.filter(num=num).exists()
        if is_user :

            validnum = random.randint(1000, 9999)
            # account_sid ='AC71c08d07ed3583edf7657ecd0040d057'
            # auth_token = '87ac49a092c370a9f358dbd11d3ed7e3'
            # client = Client(account_sid, auth_token)

            # message = client.messages.create(
            #                             body=f'OTP login - {validnum}',
            #                             from_='+1 781 661 5912',
            #                             to='+91' +num
            #                             )

            print(validnum)
            request.session['validnum'] = validnum
            request.session['num'] = num
            return render(request,"user/otp.html")

       
        

        
        else:
            messages.error(request,"This phone number is not registered",extra_tags=signin)
    return render(request,"user/login.html")


def verify(request):
    print('verify')
    if request.method == 'POST':
        print('method post')
        otp = str(request.POST['otp'])
        votp = str(request.session['validnum'])
        if votp == otp:
            print('save otp')
            num = request.session['num']
            profile = Profile.objects.get(num = num)
            user = profile.user
            print(user.username)
            auth.login(request,user)
            print('loggedin')
            return redirect('home')
        
    return redirect('userlogin')                    

           



def userprofile(request):
    return render(request,"user/profile.html")


@login_required(login_url='userlogin')
def checkout(request, total=0, quantity=0,cart_item=None):
    if request.session.has_key('num'):
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total +=(cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            delivery = 100
            grandtotal = total + delivery
            
        except ObjectDoesNotExist:
            pass
        form = AddressForm()
        queryset = Address.objects.all().filter(user=request.user)
        
        context ={
            'total' : total,
            'form' : form,
            'quantity' : quantity,
            'cart_items' : cart_items,
            'delivery' : delivery,
            'grandtotal' : grandtotal,
            'addresses' : queryset,
            
            }

        return render(request,"user/checkout.html",context)
    else:
        return redirect('userlogin')    
    

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    




def add_cart(request,id):
    product = Product.objects.get(id=id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        ) 
        cart.save()   

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart 

        )
        cart_item.save()
    request.session['num'] ='num'
    return redirect('cart')   


def remove_cart(request,id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')    

def remove_cart_item(request, id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')








def cart(request):
    cart_items=None
    total=0
    quantity=0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        
    except ObjectDoesNotExist:
        pass

    context ={
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        }

    return render(request,"user/cart.html",context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(productname__icontains=keyword) | Q(brand__icontains=keyword))
            product_count = products.count()
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request,"user/shop.html",context)





def address(request):
                                                                
   
    if request.method == 'POST':
        print('post')
        
        form = AddressForm(request.POST)
        print(form)
        
        if form.is_valid():
            print('success')
            address=form.save(commit=False)
            address.user=request.user
            address.save()
    return redirect('checkout')

    








        













                