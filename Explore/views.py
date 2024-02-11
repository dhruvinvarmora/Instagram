from typing import Any, Dict
# from django_datatables_too.mixins import DataTableMixin
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import *
from .forms import *
from post.forms import *
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.db.models import Q
from  django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from crispy_forms.utils import render_crispy_form
from allauth.account.views import SignupView,LoginView,LogoutView,PasswordChangeView
from django.contrib.auth import logout



class Search(TemplateView):
    template_name = 'Explore/Search.html' 

class SearchProfile(ListView):
    model=MyUser
    template_name = 'Explore/Search.html' 
    def get(self,request,*args,**kwargs):
        serach_profile=request.GET.get("Search")
        all_profile=MyUser.objects.filter(username__contains=serach_profile).exclude(username=request.user.username)
        context={"all_profile":all_profile}
        return render(request,self.template_name,context)
class Explore_post(ListView):
    model=Post
    template_name="Explore/explore.html"
    
    
class SerachExplorepostView(ListView):
    model=Post
    template_name="Explore/explore.html"
    def get(self,request,*args,**kwargs):
        serach_post=request.GET.get("Search")
        post_list=Post.objects.filter(captions__contains=serach_post)
        context={"all_post":post_list}
        return render(request,self.template_name,context)

