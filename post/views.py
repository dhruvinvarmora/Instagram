from audioop import reverse
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from User.models import *
from .forms import *
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.db.models import Q
from  django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from crispy_forms.utils import render_crispy_form
from allauth.account.views import SignupView,LoginView,LogoutView,PasswordChangeView
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class CreatePostView(CreateView):
    model=Post
    template_name="post/createpost.html"
    form_class=PostForm
    success_url = reverse_lazy("User:home")

    def get_context_data(self):
        context=super().get_context_data()
        context["postimg"]=PostImgForm
        return context
    def form_valid(self,form):
        post_obj = form.save()
        postimage = self.request.FILES.getlist('post_img')
        for image in postimage:
            PostImage.objects.create(post_img=image,post=post_obj)
        return super().form_valid(form)

class PostDetail(DetailView):
    model=Post
    template_name="post/postdetail.html"
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data()
        id=self.kwargs["pk"]
        posts=PostImage.objects.filter(post=id)
        context["posts"]=posts
        allcomment=Comment.objects.filter(post=id)
        context["allcomment"]=allcomment
        return context
    
class CreateCommentView(View):
    def get(self,request,*args, **kwargs):
        post_id=request.GET.get("post_id")
        user=self.request.user
        post_obj=request.GET.get("text")
        Comment.objects.create(text=post_obj,post=Post.objects.get(id=post_id),user=MyUser.objects.get(id=user.id))
        return redirect(request.META.get("HTTP_REFERER"))
    

class PostDeleteView(DeleteView):
    model=Post
    template_name="post/postdetail.html"
    def get_success_url(self):
        post= self.kwargs
        post_id=post["pk"]
        user_username=Post.objects.get(pk=post_id)
        username=user_username.user
        return reverse_lazy('User:profile', kwargs={'username': username})

class PostAddtoFavoriteView(View):
    template_name="home.html"
    def post(self,request,*args, **kwargs):
        post_id=int(request.POST.get('post_id'))
        user=self.request.user
        data=False
        data=ArchivePost.objects.filter(archive_post=post_id,user=user.id).exists()
        print("➡ data :", data)
        try:
            pass


        except Exception as e:
            pass


        if data is True:
            pass
        else:
            ArchivePost.objects.create(user=MyUser.objects.get(id=self.request.user.id), archive_post=Post.objects.get(id=post_id))
        return redirect(request.META.get("HTTP_REFERER"))

@method_decorator(login_required,name="dispatch")       
class LikeView(View):
    def post(self,request):
        user=request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"User is Not Authenticated."},status=403)
        
        post_id=request.POST.get("post_id")
        print("➡ post_id :", post_id)
        post = get_object_or_404(Post, id=post_id)

        if user in post.like.all():
            post.like.remove(user)
            is_liked =False
        else:
            post.like.add(user)
            is_liked =True

        response_data={
            "is_liked":is_liked,
            'like_count':post.like.count()
        }
        return JsonResponse(response_data)

class ShowArchive(ListView):
    model=ArchivePost
    template_name="post/showfavourite.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        favourite=ArchivePost.objects.filter(user=self.request.user.id)
        print("➡ favourite :", favourite)
        context['favourite']=favourite
        return context

class Notificitons(models.Model):
    FOLLOW="follow"
    LIKE="like"
    UNFOLLOW="unfollow"
    UNLIKE="unlike"
    UPLOADED="post"
    COMMENT="comment"
    receiver= models.ForeignKey(MyUser, on_delete=models.CASCADE ,related_name="receiver",null=True)
    post= models.ForeignKey(Post, on_delete=models.CASCADE ,related_name="receiver",null=True)
    type=models.CharField(max_length=250)
    sender=models.ForeignKey(MyUser, on_delete=models.CASCADE,related_name="sender" )
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE,related_name="comment",null=True )
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)