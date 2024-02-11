from django.core import validators
from django import forms
from post.models import *
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=["captions"]

class PostImgForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields=["post_img"]
        widgets={
            "post_img":forms.ClearableFileInput(attrs={"Multiple":True})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['text']
        widgets={
            "text":forms.TextInput()
        }