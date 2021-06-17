from django.db import models


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    cat_image = models.ImageField(upload_to='photos/categories',blank=True)

    def __str__(self):
        return self.category_name

class Size(models.Model):
   size = models.CharField(max_length=50)

class Product(models.Model):
    image1 = models.ImageField(upload_to='photos/productimages')
    image2 = models.ImageField(upload_to='photos/productimages')
    image3 = models.ImageField(upload_to='photos/productimages',blank=True)
    image4 = models.ImageField(upload_to='photos/productimages',blank=True)
    brand = models.CharField(max_length=50)
    productname = models.CharField(max_length=50,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.IntegerField()
    offers = models.IntegerField()
    newprice = models.IntegerField(default=0)
    size = models.ManyToManyField(Size, default='s')
    stock = models.IntegerField()
    
    def __str__(self):
        return self.brand



class EditProduct(models.Model):
    image1 = models.ImageField(upload_to='photos/productimages')
    image2 = models.ImageField(upload_to='photos/productimages')
    image3 = models.ImageField(upload_to='photos/productimages',blank=True)
    image4 = models.ImageField(upload_to='photos/productimages',blank=True)
    brand = models.CharField(max_length=50)
    price = models.IntegerField()
    offers = models.IntegerField()
    
    stock = models.IntegerField()
    
    def __str__(self):
        return self.price        