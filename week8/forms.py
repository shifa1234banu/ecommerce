from django import forms
from .models import Category, Product, EditProduct,Size



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','cat_image')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image1','image2','image3','image4','brand','productname','price','offers','size','stock','category')



class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields =('size',)