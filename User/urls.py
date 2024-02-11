"""
URL configuration for instagram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from User import views

from django.contrib.auth.decorators import login_required 
from django.conf import settings
app_name="User"
urlpatterns = [
    path('', login_required(views.Home.as_view()), name='home'),
    
    # ?path('', login_required(views.CreatePost.as_view()), name='createpost'),

    path('Loginprofile/<str:username>', login_required(views.ProfileView.as_view()), name='profile'),

    path('Userprofile/<str:username>', login_required(views.SearchUserProfileView.as_view()), name='Userprofile'),

    path('Edit/<str:username>/', login_required(views.UserEditProfile.as_view()), name='usereditprofile'),


    path('follow_done_view', login_required(views.Followview.as_view()), name='follow_done_view'),
    path('unfollow_done_view', login_required(views.UnFollowView.as_view()), name='unfollow_done_view'),
    path('<str:username>/follower', login_required(views.ShowFollower.as_view()), name='showfollower'),
    path('<str:username>/following', login_required(views.ShowFollowing.as_view()), name='showfollowing'),
    path('followajax', login_required(views.FollowAjax.as_view()), name='followajax'),
    path("user/fcm/token/", views.CreateUserFCMTokenAJAX.as_view(), name="user-fcm-token"),
    
    
]