from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control mb-0', 'placeholder':"Elektron pochtangizni kiriting"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-0', 'placeholder':"Username o'ylab toping"}))
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control mb-0', 'placeholder':"Esda qolishli parol yarating: 8 tagacha"}))
    password2 = forms.CharField(label='Pasword Again', widget=forms.PasswordInput(attrs={'class': 'form-control mb-0', 'placeholder':"Parolni qayta kiriting"}))
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['balance']