from django.core import validators
from django import forms

from post.models import Story
from .models import *
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

class UserRegister(UserCreationForm):
    username=forms.CharField(max_length=50,required=True,widget=forms.TextInput)
    email=forms.EmailField(max_length=50,required=True,widget=forms.EmailInput)
    password1=forms.CharField(max_length=50,required=True ,widget=forms.PasswordInput,label='Password')
    password2=forms.CharField(max_length=50,required=True,widget=forms.PasswordInput,label='Confirm Password')


    class Meta:
        model=MyUser
        fields=("username","email","password1",'password2')


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