# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from shop.models import Pedido

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        
class PedidoAdminForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcional.')
    email = forms.EmailField(max_length=254, help_text='Requerido')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )