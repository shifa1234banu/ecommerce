from django.shortcuts import render,redirect,get_object_or_404
from week8.models import Product
from week8.models import Size,Coupon,Category
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Profile,Cart,CartItem,Address,Order
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,Count
from .forms import AddressForm,ProfileForm,UserForm,ImageForm
import random
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
import datetime
import razorpay
from decouple import config
from django.views.decorators.cache import never_cache




# import os
# import random
# from twilio.rest import Client

# Create your views here.


def home(request):
    brand = Product.objects.all()
    product = Product.objects.all()
    category = Category.objects.all()
    brands = Product.objects.filter(brand=brand)
   
    for p in product:
        if p.offers > p.category.offer:
            p.newprice=int(p.price-(p.offers*p.price/100))
        elif p.offers <= p.category.offer:
            p.newprice=int(p.price-(p.category.offer*p.price/100))
        p.save()
    print(request.user.is_authenticated)
    context = {'products' : product,
               'categories': category,
               'brands':brand,
                }
    
    return render(request,"user/index.html",context)

    


def size(request):
    size = Size.objects.all()
    context = {'sizes' : size}
    return render(request,"user/productdetails.html",context)

       

def userlogin(request):
    
    return render(request,"user/login.html")


def productdetails(request, id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()
    brands = Product.objects.filter(brand=brand)
    context={'product' : product,
             'categories':categories,
             'brands': brand }
    return render(request,"user/product-details.html", context)    



  


def register(request):
      
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            num = request.POST['num']
            password = request.POST['password1']
            username = request.POST['username']
            

            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exist')
                return render(request,'user/register.html')
            elif Profile.objects.filter(num=num).exists(): 
                messages.info(request, 'phone number already exist')
                return render(request,'user/register.html')  
                
            else:
                return render(request,"user/login.html") 

            user =User.objects.create_user(first_name =first_name,last_name=last_name,email=email,password=password,username=username)
            user.save()

            
            
            
            profile = Profile()
            profile.num=num
            profile.user=user
            profile.save()
            print('working')
            # request.session['validnum'] = 'validnum'
            return redirect('home')

        return render(request,"user/register.html")



def logincheck(request):
    
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)
            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cart_item = CartItem.objects.get(cart=cart)
                    cart_item.user= user
                    cart_item.save()
                except:
                    pass    
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

            
            account_sid = config('account_sid',cast=str)
            auth_token = config('auth_token',cast=str)
            client = Client(account_sid, auth_token)
            service=config('verification',cast=str)
            verification = client.verify \
                                .services(service) \
                                .verifications \
                                .create(to='+91' +num, channel='sms')

            print(verification.status)
            

           
            
            request.session['num'] = num
            return render(request,"user/otp.html")
        else:
            messages.info(request,"This phone number is not registered")
    return render(request,"user/login.html")

def verify(request):
   
    if request.method == 'POST':
        
        otp = request.POST['otp']
        num = request.session['num']
        
        account_sid = config('account_sid')
        auth_token = config('auth_token')
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                                .services(config('verification',cast=str)) \
                                .verification_checks \
                                .create(to='+91' +num, code=otp)

        print(verification_check.status)
        if verification_check.status == 'approved':
            profile = Profile.objects.get(num=num)
            user = profile.user
        
            auth.login(request,user)
            print('loggedin')
            return redirect('home')
        
    return redirect('userlogin')                    

def otp(request):
    return render(request,"user/otp.html")  


def usercheck(request):
    return render(request,"user/profile.html")


def userprofile(request):
    
        user =request.user
        profile = Profile.objects.get(user=user)
        print(profile.userimage)

        profileform = ProfileForm(instance=profile)
        imageform = ImageForm(instance=profile)

        userform = UserForm(instance=user)
        

        if request.method == 'POST':
             print('work')
             profileform = ProfileForm(request.POST , instance=profile)
             imageform = ImageForm(request.POST , request.FILES , instance=profile)

             if imageform.is_valid():
                print('worked')
                imageform.save()
                return redirect('userprofile')

       
        context={
            'profileform' : profileform,
            'userform': userform,
            'imageform' : imageform,
            'profile':profile
         }
            
    
        return render(request,"user/profile.html",context)


def editprofile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    
    if request.method == 'POST':
        profileform = ProfileForm(request.POST,instance = profile)
        userform = UserForm(request.POST,instance = user)
        print('valid check')
        if userform.is_valid() and profileform.is_valid():
            profileform.save()
            userform.save()
            return redirect('userprofile')
        else:
            profileform = ProfileForm(instance = profile)
            userform = UserForm(instance = user)
            return redirect('userprofile')
                    

@never_cache
@login_required(login_url='userlogin')
def checkout(request, total=0, quantity=0,cart_item=None,sub_total=0):
    if request.session.has_key('num'):
        cart_items = None
        try:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            for cart_item in cart_items:
                total +=(cart_item.product.newprice * cart_item.quantity)
                sub_total = cart_item.product.newprice * cart_item.quantity 
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
            'sub_total' : sub_total,
            
            }

        return render(request,"user/checkout.html",context)
    else:
        return redirect('userlogin')    
    
@never_cache
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    

@never_cache
def cart(request):
    user=request.user
    cart_items=None
    total=0
    quantity=0
    
    try:
        cart_items = CartItem.objects.filter(user=user, is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.newprice * cart_item.quantity)
            sub_total = cart_item.product.newprice * cart_item.quantity
            quantity += cart_item.quantity
        
    except ObjectDoesNotExist:
        pass

    context ={
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        }
    return render(request,"user/cart.html",context)


login_required(login_url='userlogin')
@never_cache
def add_cart(request):
    id = int(request.GET['id'])
   
    user = request.user
    product = Product.objects.get(id=id)

    try:
        cart_item = CartItem.objects.get(product=product, user=user)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            user=user
        )
        cart_item.save()
    request.session['num'] ='num'
    return JsonResponse({'data':True})


def remove_cart(request,total=0):
    product_id = int(request.POST['product_id'])
    cart_id = int(request.POST['cart_id'])
    
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, user=request.user)
    if cart_item.quantity > 1:
        print('work')
        cart_item.quantity -= 1
        cart_item.save()
        total += (cart_item.product.newprice * cart_item.quantity)
    else:
        CartItem.objects.filter(product=product,user=request.user).delete()
    data = {'total':total,'cart_id':cart_id}
    return JsonResponse(data)  

def update_cart(request,total=0,subtotal=0):
    cart_id = int(request.POST['cart_id'])
    product_id = int(request.POST['pro_id'])
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, user=request.user)
    try:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            subtotal +=(cart_item.product.newprice * cart_item.quantity-1)
            print(subtotal)
        cart_item = CartItem.objects.get(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        total += cart_item.product.newprice * cart_item.quantity+1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart 
        )
        cart_item.save()
    data = {'total':total,'quantity':cart_item.quantity,'cart_id':cart_id,}
    return JsonResponse(data)

def remove_cart_item(request,id):
    CartItem.objects.filter(id=id).delete()
    return redirect('cart')











def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(productname__icontains=keyword) | Q(brand__icontains=keyword))
            product_count = products.count()
        else:
            return render(request,"user/index.html")    
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request,"user/shop.html",context)





def address(request):
                                                                
   
    if request.method == 'POST':
      
        
        form = AddressForm(request.POST)
        print(form)
        
        if form.is_valid():
            print('success')
            address=form.save(commit=False)
            address.user=request.user
            address.save()

            
    return redirect('checkout')

    
@never_cache
def place_order(request):
    print('hi')
    total=0
    quantity=0
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    if cart_items.exists():
        for cart_item in cart_items:
            total +=(cart_item.product.newprice * cart_item.quantity)
            quantity += cart_item.quantity
        
        delivery = 100
        grandtotal = total + delivery

        request.session['grandtotal'] =  grandtotal
        if request.session.has_key('total2'):
            subtotal = request.session['total2'] * 100
            print(subtotal)
            # del request.session['total2']
        else:
            subtotal = grandtotal * 100
        request.session['subtotal'] = subtotal
        print(request.session['subtotal'])

        try:
            address_id =(request.POST.get('address'))
            bill_address = Address.objects.get(id=address_id)
        except:
            bill_address=None
            return redirect('checkout')
        amount=request.session['subtotal']
        rupee= float(amount)*100
        order_currency = 'INR'
        client = razorpay.Client(auth=("rzp_test_krpej6LVaGfmNT", "sPVzxFmh0PyMnAvMkXrS1Qs0"))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                    'payment_capture': '1'})
        request.session['payment_method'] = 'razorpay'                               
        # print(request.session['payment_method']) 
        context ={
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cart_items,
            'delivery' : delivery,
            'grandtotal' : grandtotal,
            'subtotal': subtotal,
            'bill_address': bill_address,
            'amount':amount,
            'rupee':rupee,
            
            }

    
        return render(request,"user/placeorder.html",context)
    else:
        return redirect('home') 


@never_cache
def razorsuccess(request,total=0):

        
        # cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.newprice * cart_item.quantity)
            amount = total+100
       
    
            pay_method = request.session['payment_method']
            order = Order.objects.create(user=request.user,item=cart_item.product,price=(cart_item.product.newprice * cart_item.quantity),pay_method=pay_method)
            order.save()
            cart_item.delete()
    
        return render(request,"user/success.html")        


def myorder(request):
    user=request.user
    Order.objects.all().delete()
    order = Order.objects.filter(user=user)
   
   
    context = {
        'user': user,
        'order' : order,
        
        }
    
    
    return render(request,"user/myorder.html",context)

@never_cache  
def paypal(request,total=0):
    total=0
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    for cart_item in cart_items:
        total += (cart_item.product.newprice * cart_item.quantity)
    amount = total+100
    pay_method = 'paypal'
    order = Order.objects.create(user=request.user,item=cart_item.product,price=amount,pay_method=pay_method)
    
    order.save()
    cart_item.delete()
    return render(request,"user/success.html")

@never_cache
def couponcheck(request,total=0,quantity=0):
    if request.method == 'POST':
        
        print(cart)
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.newprice * cart_item.quantity)
            quantity += cart_item.quantity
        
        delivery = 100
        grandtotal = total + delivery
        print('work')
        coupon = request.POST['code']
        if Coupon.objects.filter(coupon_code=coupon).exists():
            obj = Coupon.objects.get(coupon_code=coupon)
            dis = obj.coupon_offer
            discount = dis*total/100
            print(discount)
            balance = grandtotal-discount
            
            request.session['total1'] = discount
            request.session['total2'] = balance

            context = {
                'total':"% .2f" % discount,
                'code': coupon,
                'grandtotal': "% .2f" % balance,
                
            }
            print(grandtotal)
            return JsonResponse(context)
        return JsonResponse("false",safe=false)    




def logout(request):
    auth.logout(request)
    return redirect('/')



def catformal(request,id):
    category = Category.objects.get(id=id)
    pro = Product.objects.filter(category=category)
    context={'pro' : pro}
    return render(request,"user/category.html",context)   


def brand(request,bar):
    brand = Product.objects.filter(brand=bar)
    
    context={'br' : brand}
    return render(request,"user/brand.html",context) 




    
# if request.method == 'POST':
        
#             first_name = request.POST['first_name']
#             email = request.POST['email']
#             username = request.POST['username']
#             password = request.POST['password']
        
#             User.objects.filter(pk=user_id).update(first_name=first_name,email=email,username=username,password=password)
            
#             return redirect('ad_user')
#         else:
#             return redirect('ad_edit')


def delete_order(request,id):
    order = Order.objects.get(pk=id)
    order.status = 'Cancelled'
    order.save()
    return redirect('/myorder')       
    
    





        













                