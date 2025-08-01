from django.core import validators
from django import forms

from post.models import Story
from .models import *
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import SignupForm


class Userlogin(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        })
    )
class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput())
    email = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput())
    
    def save(self, request):
        user = super().save(request)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()
        return user

class Userlogin(forms.ModelForm):
    username=forms.CharField(max_length=50,required=True,widget=forms.TextInput)
    password=forms.CharField(max_length=50,required=True ,widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields=('email','password')

class UserChangPass(PasswordChangeForm):
    # old_password=forms.CharField(max_length=30, required=True,widget=forms.PasswordInput,label='Old Password')
    # new_password1=forms.CharField(max_length=30, required=True,widget=forms.PasswordInput,label='New Password')
    # new_password2=forms.CharField(max_length=30, required=True,widget=forms.PasswordInput,label='Confirm Password')
    class Meta:
        model=MyUser
        fields=("old_password","new_password1","new_password2")



class ProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields=("first_name","last_name","Bio","username","email","Gender","DP")


        
class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['story']