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
        All_following_user = Follow.objects.filter(followed=user,follow_each_other=True)
        posts = Post.objects.all()
        context['-------------All_following_user-------------'] = All_following_user
        following_users= Follow.objects.filter(user=user,follow_each_other=True)
        context["All_following_user"] = following_users
        print('--->>>>>>following_users: ', following_users)
        # for following_user in following_users:
        #     room_name1=f"chat_{following_user.user.username}_{following_user.followed.username}"
        #     print('room_name1: ', room_name1)
        #     room_name2=f"chat_{following_user.followed.username}_{following_user.user.username}"
        #     print('room_name2: ', room_name2)
        #     rooms = Room.objects.filter(Q(name=room_name1) | Q(name=room_name2))
        #     for room in rooms:
        #         if room.name == room_name1:
        #             print("------in if--------")
        #             print('room.name: ', room.name)
        #             user1=room.nameslplit(chat_)
        #         else:
        #             print("-in else----")
        #             print('room.name: ', room.name)
        #     print('rooms: ', rooms)
        following_user_dict = {}
        rooms = []  # ✅ initialize rooms to avoid UnboundLocalError

        for following_user in following_users:
            room_name1 = f"chat_{following_user.user.username}_{following_user.followed.username}"
            room_name2 = f"chat_{following_user.followed.username}_{following_user.user.username}"
            
            matched_rooms = Room.objects.filter(Q(name=room_name1) | Q(name=room_name2))
            for room in matched_rooms:
                if room.name == room_name1:
                    user1_username, user2_username = following_user.user.username, following_user.followed.username
                else:
                    user1_username, user2_username = following_user.followed.username, following_user.user.username
                
                user1_obj = MyUser.objects.get(username=user1_username)
                user2_obj = MyUser.objects.get(username=user2_username)

                if self.request.user.username == user1_username:
                    following_user_dict[room] = user2_obj
                else:
                    following_user_dict[room] = user1_obj
                
                rooms.append(room)  
        print('following_user_dict: ', following_user_dict)
        context["All_following_user"] = following_users
        context["following_user_dict"] = following_user_dict
        context['rooms'] =rooms
        context['posts'] = posts
        context['story_form'] = StoryForm()
        messages=Message.objects.all()
        print('----------------messages: ', messages)
        context['messages'] = messages
        notificion=Notificitons.objects.all().order_by("-id")
        context["notificions"]=notificion
        user_stories_dict = {}
        context['user_stories_dict'] = user_stories_dict
        return context

# def rooms(request):
#     rooms=Room.objects.all()
#     return render(request, "rooms.html",{"rooms":rooms})

class Chat(TemplateView):
    # template_name = 'room.html'
    template_name = 'chat_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        print('slug: ', slug)
        
        # Split the slug to get the usernames
        user1_username, user2_username = slug.split('_')
        
        # Retrieve the user objects from the database
        user1 = MyUser.objects.get(username=user1_username)
        user2 = MyUser.objects.get(username=user2_username)
        print('user1: ', user1)
        print('user2: ', user2)
        
        # Check which user is the logged-in user
        if self.request.user != user1:
            context["user"] = user1
        else:
            context["user"] = user2
        room = Room.objects.filter(slug=slug).first()
        print('room:-------- ', room)
        if room:
            context['room_name'] = room.name
            Message.objects.filter(room=room)
            print('Message.objects.filter(room=room): ', Message.objects.filter(room=room))
            context['messages'] = Message.objects.filter(room=room).order_by('-created_on')
        else:
            print("-in else----")
            # Handle the case where the room with the given slug doesn't exist
            # You can redirect to an error page or do something else
            pass
        return context
class RoomView(TemplateView):
    # template_name = 'messages.html'
    template_name = 'rooms.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        following_users= Follow.objects.filter(followed=user)
        print('following_users: ', following_users)
        context["All_following_user"] = following_users
        rooms =Room.objects.filter(slug__in=[following_user.user.username for following_user in following_users])
        print('rooms: ', rooms)
        context['rooms'] =rooms

        return context
    
class Reels(TemplateView):
    template_name = 'Explore/reels.html'

#-----------------------------Authentication----------------------------------#
class Register(SignupView):
    form_class = CustomSignupForm
    template_name = "Authentication/register.html"
    success_url = reverse_lazy("userlogin")

class UserLogin(LoginView):
    template_name = 'Authentication/login.html'
    authentication_form = Userlogin
    redirect_authenticated_user = True  

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
# class Followview(View):
#     template_name="UserDetail.html"
#     def post(self,request,*args,**kwargs):
#         followed_user_id=request.POST.get("follow_user_id")
#         followed_user_obj=MyUser.objects.get(pk=followed_user_id)
#         print('followed_user_obj: ', followed_user_obj)
        
#         room_name=f'chat_{followed_user_obj}_{self.request.user.username}'
#         slug=followed_user_obj
        
#         try:
#             Follow.objects.get(user=request.user,followed=followed_user_obj)
#         except Exception as e:
#             Follow.objects.create(followed=followed_user_obj)
        


#         room_name = f'chat_{followed_user_obj}_{self.request.user.username}'
#         slug = f'{followed_user_obj}_{self.request.user.username}'

#         # Check if both users follow each other
#         if Follow.objects.filter(user=request.user, followed=followed_user_obj).exists() and \
#         Follow.objects.filter(user=followed_user_obj, followed=request.user).exists():
#             follow1 = Follow.objects.get(user=request.user, followed=followed_user_obj)
#             follow2 = Follow.objects.get(user=followed_user_obj, followed=request.user)
            
#             follow1.follow_each_other = True
#             follow2.follow_each_other = True
            
#             follow1.save()
#             follow2.save()
            
#             room = Room.objects.create(slug=slug, name=room_name)
#             print('room: ', room)

#         try:
#             token = FCMDevice.objects.filter(user_id=self.request.user.id).first()
#         except Exception as e:
#             print("e",e)

#         # fcm_message = {
#         #         "message": {
#         #             "token": token,
#         #             "notification": {"title": message_title, "body": message_body},
#         #             "webpush": {"fcm_options": {"link": settings.APP_URL}},
#         #         }
#         #     }
#         # send_notification(
#         #     user=self.request.user,
#         #     token=token.device_id if token else " ",
#         #     message_title="Task",
#         #     message_body=f" Task Created Successfully",
#         # )
        
#         user_ids = [followed_user_obj.id]
#         data = {"title": "Title", "message": f"{self.request.user} Started Following You"}
#         send_firebase_push_notification(user_ids, data)

#         return redirect(request.META.get("HTTP_REFERER"))

class Followview(View):
    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get("follow_user_id")
        followed_user_obj = MyUser.objects.get(pk=followed_user_id)

        # Prevent duplicate
        _, created = Follow.objects.get_or_create(user=request.user, followed=followed_user_obj)

        if created:
            # Optional: send notification
            user_ids = [followed_user_obj.id]
            data = {"title": "New Follower", "message": f"{request.user.username} started following you."}
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
