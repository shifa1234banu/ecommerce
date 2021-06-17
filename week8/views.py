from django.shortcuts import render,redirect
from .forms import CategoryForm,ProductForm,SizeForm
from .models import Category
from .models import Product
from .models import Size
from django.contrib.auth.models import User,auth
from zehak.models import Profile





# Create your views here.


def login(request):
    return render(request,"admin/login.html")

def adhome(request):
    return render(request,"admin/index.html")    


def user(request):
    
    queryset = Profile.objects.all()
    context = {'profiles' : queryset}
    return render(request,"admin/user.html",context)
    



def logout(request):
   
        auth.logout(request)
        request.session.flush()
        return redirect('/')
        

def product(request):
    products = Product.objects.all()
    
    return render(request,"admin/product.html", {'products' : products})
    



def addproduct(request):

    if request.method == 'POST':
        offerprice=0
        form = ProductForm(request.POST, request.FILES)
        
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




def category(request):
    
    categories = Category.objects.all()
    return render(request,"admin/category.html", {'categories' : categories})

    

def addcategory(request):
   
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
        

    
    
        

    
def editproduct(request, id):
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


def deleteproduct(request, id):
    

        product = Product.objects.get(pk=id)
        return render(request,'admin/productdelete.html' ,{'product' : product}) 
    


def deletecheck(request, id):
    

        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('product')




def blockuser(request, id):
    user=User.objects.get(pk=id)
    user.is_active = False
    user.save()

    return redirect('user')


def unblockuser(request, id):
    user=User.objects.get(pk=id)
    user.is_active = True
    user.save()

    return redirect('user')    


def categorycheck(request, id):
    

        category = Category.objects.get(pk=id)
        category.delete()
        return redirect('category')    


def deletecategory(request, id):
    

        category = Category.objects.get(pk=id)
        return render(request,'admin/categorydelete.html' ,{'category' : category})        