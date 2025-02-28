from django import forms
from .models import *



# class Shop_panelEditForm(forms.ModelForm):
#     class Meta:
#         model = Shop_panel
#         fields = ['first_name', 'last_name','phone', 'image']

class RequestUserForm(forms.ModelForm):
    class Meta:
        model = RequestU
        fields = ['text']


class ProfileShopEditForm(forms.ModelForm):
    class Meta:
        model = Shop_panel_profile
        fields = ['name_of_shop', 'desc', 'avatar', 'adress', 'phone_of_owner','phone_of_shop' , 'code_melli_of_owner']


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','slug','image', 'price','desc', 'tedad', 'category','status','num']