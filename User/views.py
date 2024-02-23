from typing import Any, Dict
# from django_datatables_too.mixins import DataTableMixin
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView

from User.utils import send_firebase_push_notification
from post.views import Notificitons
from post.tasks import delete_old_stories
from .models import *
from post.models import *
from .forms import *
from post.forms import *
from post.forms import *
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.db.models import Q
from  django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from crispy_forms.utils import render_crispy_form
from allauth.account.views import SignupView,LoginView,LogoutView,PasswordChangeView
from django.contrib.auth import logout
from crum import get_current_user
from fcm_django.models import FCMDevice


class Home(TemplateView):
    template_name = 'home.html'
# class Explore(TemplateView):
#     template_name = 'Explore/explore.html'

class Messages(TemplateView):
    template_name = 'messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        All_following_user = Follow.objects.filter(user=user)
        first_All_following_user = Follow.objects.filter(user=user).first()
        print('first_All_following_user: ', first_All_following_user)
        posts = Post.objects.all()
        context['All_following_user'] = All_following_user
        context['first_All_following_user'] = first_All_following_user.user.username

        context['posts'] = posts
        context['story_form'] = StoryForm()
        notificion=Notificitons.objects.all().order_by("-id")
        context["notificions"]=notificion
        user_stories_dict = {}
        context['user_stories_dict'] = user_stories_dict
        return context



class Reels(TemplateView):
    template_name = 'Explore/reels.html'

#-----------------------------Authentication----------------------------------#
class Register(SignupView):
    form_class = UserRegister
    template_name = "Authentication/register.html"
    success_url = reverse_lazy("userlogin")

class UserLogin(LoginView):
    authentication_form = Userlogin
    template_name = 'Authentication/login.html'

class Logout(LogoutView):
    def get(self,request):
        logout(self.request)
        return redirect('userlogin')

class UserChangePassword(PasswordChangeView):
    form_class=UserChangPass
    template_name="Authentication/ChangePassword.html"
    success_url = reverse_lazy("home")



#-------------------------------Main-Pages---------------------------------#
class Home(TemplateView):
    template_name = "home.html"
    form_class = StoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        All_following_user = Follow.objects.filter(user=user).values_list('followed', flat=True)
        suggestpeople = MyUser.objects.all().exclude(id__in=list(All_following_user)).exclude(username=user)
        posts = Post.objects.all()
        context['All_following_user'] = All_following_user
        context['suggestpeople'] = suggestpeople
        context['posts'] = posts
        context['story_form'] = StoryForm()
        stories = Story.objects.filter(
        user__in=All_following_user) | Story.objects.filter(user=get_current_user())
        notificion=Notificitons.objects.all().order_by("-id")
        print('notificion--------------------------------------------: ', notificion)
        context["notificions"]=notificion
        context['stories'] = stories
        user_stories_dict = {}
        stories = Story.objects.filter(user__in=All_following_user) | Story.objects.filter(user=user)
        delete_old_stories()
        for story in stories:
            if story.user not in user_stories_dict:
                user_stories_dict[story.user] = []
            user_stories_dict[story.user].append(story)

        context['user_stories_dict'] = user_stories_dict
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('home')  # Redirect to home page after successful submission
        else:
            # Handle form errors
            context = self.get_context_data()
            context['story_form'] = form
            return self.render_to_response(context)
class UserSetting(TemplateView):
     template_name = 'setting.html'


   

#_----------------------------Follow-UnFollow---------------------#
class FollowAjax(View):
    def post(self,request,*args,**kwargs):
        id=request.POST.get("id")
        followed_user_obj=MyUser.objects.get(pk=id)

        try:
            Follow.objects.get(user=request.user,followed=followed_user_obj)
        except Exception as e:
            Follow.objects.create(followed=followed_user_obj)
            
        Unfollow="" 
        response_data={
            Unfollow:"True"
        }
        return JsonResponse(response_data)


    
class UnFollowView(View):
     def post(self,request,*args,**kwargs):
        unfollowed_user_id=request.POST.get("unfollow_user_id")
        unfollowed_user_obj=MyUser.objects.get(pk=unfollowed_user_id)
        try:
            follow_obj=Follow.objects.get(user=request.user,followed=unfollowed_user_obj)
            follow_obj.delete()
        except Exception as e:
            pass
        return redirect(request.META.get("HTTP_REFERER"))

class ShowFollower(ListView):
    model=MyUser
    template_name="User/show_follower.html"
    def get(self,request,*args, **kwargs):
        
        username=kwargs.get("username")
        user_id=MyUser.objects.get(username=username)
        data=Follow.objects.filter(followed=user_id)
        context={"all_follower":data,'id':id}
        return render(request,self.template_name,context,)
    
class ShowFollowing(View):
    model=MyUser
    template_name="User/show_follower.html"
    def get(self,request,*args, **kwargs):
        username=kwargs.get("username")
        user_id=MyUser.objects.get(username=username)
        data=Follow.objects.filter(user=user_id)
        context={"all_following":data,"id":id}
        return render(request,self.template_name,context)
    
class UserEditProfile(UpdateView):
    model=MyUser
    form_class=ProfileForm
    template_name="User/EditProfile.html"   
    slug_field = "username"
    slug_url_kwarg = 'username'
    query_pk_and_slug =True  
    success_url=reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)   
        context["img"]=MyUser.objects.filter(id=self.request.user.id  )
        user_name = self.kwargs["username"]
        return context
   
class PostDetail(ListView):
    model=PostImage
    template_name="postdetail.html"
    def get(self,request,*args, **kwargs):
        id=kwargs.get("id")
        posts=PostImage.objects.filter(post=id)
        context={"posts":posts}
        return render(request,self.template_name,context)

class ProfileView(DetailView):
    model=MyUser
    template_name="User/profile.html"
    slug_field = "username"
    slug_url_kwarg = 'username'
    query_pk_and_slug =True

    def get(self,request,**kwargs):
        username=kwargs.get("username")
        print("➡ username :", username)
        id=MyUser.objects.get(username=username)
        mypost = Post.objects.filter(user=id)
        context={"mypost":mypost}
        return render(request,self.template_name,context)
    


class SearchUserProfileView(DetailView):
    model=MyUser
    template_name="User/UserDetail.html"
    slug_field = "username"
    slug_url_kwarg = 'username'
    query_pk_and_slug =True

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(**kwargs)
        data=self.kwargs
        username=data['username']
        myuser=MyUser.objects.get(username=username)
        myuser_id=myuser.id
        mypost = Post.objects.filter(user=myuser)
        login_user = get_current_user()
        is_follow_this_user=False
        context["mypost"]=mypost
        for loged_in_user in login_user.follow_follower.all():
            if myuser_id == loged_in_user.followed.id:
                is_follow_this_user=True
                context["is_follow_this_user"]=is_follow_this_user
        return context
     
#-------------------------------Profile---------------------------------#
# class Profile(View):
#     model=User
#     template_auth_name = 'profile.html'
#     template_anon_name = 'UserDetail.html'
#     def get(self,request,*args, **kwargs):
#         main_id=kwargs.get("id")
#         mypost=Post.objects.filter(user=main_id)
#         try:
#             user=User.objects.get(pk=main_id)
            
#         except Exception as e:
#             return HttpResponse("<h1>Page Not Found</h1>")

#         context={"user":user,"mypost":mypost}
#         if main_id == request.user.id:
#             return render(request,self.template_auth_name,context)
#         else:
#             is_follow_this_user=False
#             for loged_in_user in request.user.follow_follower.all():
#                 if user == loged_in_user.followed:
#                     is_follow_this_user=True
#                     context={"user":user,"is_follow_this_user":is_follow_this_user}
#             return render(request,self.template_anon_name,context)
class Followview(View):
    template_name="UserDetail.html"
    def post(self,request,*args,**kwargs):
        followed_user_id=request.POST.get("follow_user_id")
        followed_user_obj=MyUser.objects.get(pk=followed_user_id)

        try:
            Follow.objects.get(user=request.user,followed=followed_user_obj)
        except Exception as e:
            Follow.objects.create(followed=followed_user_obj)
        token = FCMDevice.objects.filter(user_id=self.request.user.id).first()

        # fcm_message = {
        #         "message": {
        #             "token": token,
        #             "notification": {"title": message_title, "body": message_body},
        #             "webpush": {"fcm_options": {"link": settings.APP_URL}},
        #         }
        #     }
        # send_notification(
        #     user=self.request.user,
        #     token=token.device_id if token else " ",
        #     message_title="Task",
        #     message_body=f" Task Created Successfully",
        # )
        
        user_ids = [followed_user_obj.id]
        data = {"title": "Title", "message": f"{self.request.user} Started Following You"}
        send_firebase_push_notification(user_ids, data)

        return redirect(request.META.get("HTTP_REFERER"))


class CreateUserFCMTokenAJAX(View):
    """Creating FCM token for login user"""

    def post(self, request):
        user_email = request.POST.get("user_email")
        token = request.POST.get("token")
        print("--------------------------------in post section -------------------------------")
        user = MyUser.objects.filter(email=user_email).first()
        fcm = FCMDevice.objects.filter(user=user).first()

        if user and fcm:
            fcm.delete()
            FCMDevice.objects.create(
                user_id=user.id, device_id=token, registration_id=token
            )
        else:
            FCMDevice.objects.create(
                user_id=user.id, device_id=token, registration_id=token
            )

        return JsonResponse({"data": "success"})
        
class ShowFireBaseJS(View):
    def get(self, request, *args, **kwargs):
        data = (
            'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");'
            'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); '
            "var firebaseConfig = {"
            f'        apiKey:"AIzaSyDrH0S8A8u5qn7jBaVH4jHqTFCMoISOncU",'
            f'        authDomain: "instello-5ed0e.firebaseapp.com",'
            f'        projectId: "instello-5ed0e",'
            f'        storageBucket: "instello-5ed0e.appspot.com",'
            f'        messagingSenderId: "1035049981038",'
            f'        appId: "1:1035049981038:web:4f79d51698930937fb027f",'
            f'        measurementId: "G-HMDGZL5ZHZ"'
            " };"
            "firebase.initializeApp(firebaseConfig);"
            "const messaging=firebase.messaging();"
            "messaging.setBackgroundMessageHandler(function (payload) {"
            "    const notification=JSON.parse(payload);"
            "    const notificationOption={"
            "        body:notification.body,"
            "        icon:notification.icon"
            "    };"
            "    return self.registration.showNotification(payload.notification.title,notificationOption);"
            "});"
        )

        return HttpResponse(data, content_type="text/javascript")
