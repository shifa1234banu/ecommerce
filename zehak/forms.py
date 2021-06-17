from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('first_name','email','address1','address2','mobilenumber','post','landmark','country')



    def __init__(self, *args ,**kwargs):
        super(AddressForm,self).__init__(*args ,**kwargs)
        



        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'