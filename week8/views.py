from django.shortcuts import render,redirect
from .forms import CategoryForm,ProductForm,SizeForm,CouponForm
from .models import Category
from .models import Product
from .models import Size
from .models import Coupon
from django.contrib.auth.models import User,auth
from zehak.models import Profile,Order
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test




# Create your views here.


def logincheck(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('ad_home')
            else:
                messages.info(request, 'invalid credentials')
                return redirect('adlogin')
        else:
            return redirect('adlogin')



def login(request):
    return render(request,'admin/login.html')



@login_required()
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def ad_home(request):
    total=0
    totalorder = Order.objects.all().count()
    totaluser = User.objects.all().count()
    totalproduct = Product.objects.all().count()
    totalor = Order.objects.all()
   
    for i in totalor:
        total += int(i.price)


    order_placed = Order.objects.filter(status='Placed').count()
    order_shipped = Order.objects.filter(status='Shipped').count() 
    order_delivered = Order.objects.filter(status='Delivered').count()
    


    context ={
        'totalorder' : totalorder,
        'totaluser' : totaluser,
        'totalproduct' : totalproduct,
        'total' : total,
        'order_placed' : order_placed,
        'order_shipped' : order_shipped,
        'order_delivered' : order_delivered,
        
    }
    return render(request,"admin/index.html",context)        



@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def user(request):
    
    queryset = Profile.objects.all()
    context = {'profiles' : queryset}
    return render(request,"admin/user.html",context)
    


@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def ad_logout(request):
        auth.logout(request)
        request.session.flush()
        return redirect('adlogin')
   
   
        
        
@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def product(request):
    products = Product.objects.all()
    
    return render(request,"admin/product.html", {'products' : products})
    


@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def add_product(request):

    if request.method == 'POST':
        offerprice=0
        form = ProductForm(request.POST, request.FILES)
        print(form)

        if form.is_valid():
            form.save()
            price = form.cleaned_data.get('price')
            offer = form.cleaned_data.get('offers')
            productname = form.cleaned_data.get('productname')
            offerprice = (price * (offer/100))
            newprice = (price - offerprice)
            product = Product.objects.get(productname=productname)
            product.newprice = newprice
            product.save()
            print(product.newprice)
            return redirect('product')
        else:
            form = ProductForm()
            context ={'form':form}
            return render(request,"admin/addproduct.html",context)
                

    
    else:
        
        form = ProductForm()
        context ={'form':form}

        return render(request,"admin/addproduct.html",context)
    

@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def addsize(request):
    if request.method == 'POST':
        
        form = SizeForm(request.POST)
        
        if form.is_valid():
            form.save()
            print('working')
            return redirect('product')

    
    else:
        form = SizeForm()
        context ={'form':form}

        return render(request,"admin/addsize.html",context)



@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def category(request):
    
    categories = Category.objects.all()
    return render(request,"admin/category.html", {'categories' : categories})

    
@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def add_category(request):
   
    if request.method == 'POST':
        
        form = CategoryForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            print('working')
            return redirect('category')

    
    else:
        form = CategoryForm()
        context ={'form':form}

        return render(request,"admin/addcategory.html",context)


@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def edit_category(request,id):
    category = Category.objects.get(pk=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance = category)
        
        if form.is_valid():
            form.save()
            print('working')
            return redirect('category')

        

    else:
        form = CategoryForm(instance = category)
        return render(request,"admin/editcategory.html" ,{'form' : form ,'category' : category})


    
    
        

@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')   
def edit_product(request, id):
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,instance = product)
        
        if form.is_valid():
            form.save()
            print('working')
            return redirect('product')
           

        

    else:
        form = ProductForm(instance = product)
        return render(request,"admin/editproduct.html" ,{'form' : form ,'product' : product})

@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def delete_product(request, id):
    

        product = Product.objects.get(pk=id)
        return render(request,'admin/productdelete.html' ,{'product' : product}) 
    

@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def delete_check(request, id):
    

        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('product')



@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def block_user(request, id):
    user=User.objects.get(pk=id)
    user.is_active = False
    user.save()

    return redirect('user')

@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def unblock_user(request, id):
    user=User.objects.get(pk=id)
    user.is_active = True
    user.save()

    return redirect('user')    

@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def category_check(request, id):
    

        category = Category.objects.get(pk=id)
        category.delete()
        return redirect('category')    

@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def delete_category(request, id):
    

        category = Category.objects.get(pk=id)
        return render(request,'admin/category.html' ,{'category' : category})        


@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def order(request):
    orders =Order.objects.all()
    context = {'orders':orders}
    return render(request,"admin/order.html",context)       


    

@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def admin_order_status(request):
    order_id = request.POST['order_id']
    value = request.POST['clicked']
    this_order = Order.objects.get(pk=order_id)
    if request.POST['clicked'] == 'Shipped':
        this_order.status = 'Shipped'
        this_order.save()
    elif request.POST['clicked'] == 'Delivered':
        this_order.status = 'Delivered'
        this_order.save()
    return JsonResponse('true', safe=False)



@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def coupon(request):
    coupons = Coupon.objects.all()
    categories = Category.objects.all()
    return render(request,"admin/coupon.html",{'coupons' : coupons ,'categories' : categories})




@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def add_coupon(request): 
    if request.method == 'POST':

        
       form = CouponForm(request.POST)
        
       if form.is_valid():

          form.save()
          print('working')
          return redirect('coupon')

    
    else:
        form = CouponForm()
        context ={'form':form}

        return render(request,"admin/addcoupon.html",context)


@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def category_offer(request,id):
    cat = Category.objects.get(pk=id)
    
    if request.method == 'POST':
        offer = request.POST['offer']
        cat.offer=offer
        cat.save()
        return redirect('coupon')

    context = {
        'category':cat,
    }
    return render(request,"admin/addoffer.html")

    # return render(request,"admin/addcoupon.html",context)


@login_required(login_url='adlogin')
@user_passes_test(lambda user: user.is_superuser,login_url='adlogin')
def sale(request,total=0, quantity=0, cart_items=None):
    
    if request.method == 'POST':
          date_from=request.POST['datefrom']
          date_to=request.POST['dateto']
          order_search=Order.objects.filter(order_date__range=[date_from,date_to])
          return render(request,'admin/sale.html',{'orders':order_search})
    else:
        orders = Order.objects.all()
        return render(request, "admin/sale.html",{'orders':orders})
        

      

