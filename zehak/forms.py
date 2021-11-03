from django import forms
from .models import Address,Order,Profile,User

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('num',)


   
class ImageForm(forms.ModelForm):
    userimage = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ('userimage',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')      

    def __init__(self, *args ,**kwargs):
        super(UserForm,self).__init__(*args ,**kwargs)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('first_name','email','address1','address2','mobilenumber','post','landmark','country')



    def __init__(self, *args ,**kwargs):
        super(AddressForm,self).__init__(*args ,**kwargs)
        



        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    # def save(self,*args,)










