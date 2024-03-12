# forms.py
from django import forms
from django.contrib.auth.models import User



class UserDeleteForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)

class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)

class ProductDeleteForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
# forms.py
class UserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}
