# this file was not pre-built, is made to create login and registration page using prebuilt assets and changing the look of default admin page  
from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import Customer


class CustomerCreationForm(UserCreationForm): 
# instead of using botstrap, we can use django inbuilt userCreationForm
# this creating form helps us creating registeration, login, logout page  
    password1= forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'})) # here attrs= attributes, from bootstrap we get form-control
    password2= forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email= forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

class Meta():
    model= User
    fields= ['username', 'email', 'password1', 'passowrd2']
    labels= {'email':'Email'}
    widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):  # login forms dont store data, it takes data from registerations forms
    username= UsernameField(widget= forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password= forms.CharField(label=_('Password'), strip=False, widget= forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'})) 


class MyPasswordChangeForm(PasswordChangeForm):
    old_password= forms.CharField(label=_('Old Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}))
    new_password= forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))
    help_text= password_validation.password_validators_help_text_html()
    new_password2= forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email= forms.EmailField(label=_('Email'), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1= forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs= {'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs= {'autocomplete':'new-password', 'class':'form-control'}))


class MyPasswordResetConfirmForm(PasswordResetForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model= Customer # taken from models.py  class Customer
        fields= ['name', 'locality', 'city', 'state', 'zipcode']
        widgets= {'name':forms.TextInput(attrs={'class':'form-control'}), 'locality':forms.TextInput(attrs={'class':'form-control'}), 'city':forms.TextInput(attrs={'class':'form-control'}), 'state':forms.Select(attrs={'class':'form-control'}), 'zipcode':forms.NumberInput(attrs={'class':'form-control'})}        
