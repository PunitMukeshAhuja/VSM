from django import forms
from django.contrib.auth.models import User
from .models import Transaction

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class BuyForm(forms.ModelForm):

	class Meta:
		model= Transaction
		fields=['purchase_quantity']
		
class SellForm(forms.ModelForm):

	class Meta:
		model= Transaction
		fields=['sale_quantity']

		