from django import forms
from .models import Category, Product,Size,Coupon





class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','offer')
    def __init__(self, *args ,**kwargs):
        super(CategoryForm,self).__init__(*args ,**kwargs)
        



        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'    


       




class ProductForm(forms.ModelForm):
    image1 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    image2 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    image3 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    image4 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = ('image1','image2','image3','image4','brand','productname','price','offers','newprice','size','stock','category')



class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields =('size',)


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields ='__all__'  




    def __init__(self, *args ,**kwargs):
        super(CouponForm,self).__init__(*args ,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'       