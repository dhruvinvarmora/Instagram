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
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('User/', include('User.urls')),
    path('Explore/', include('Explore.urls')),
    path('accounts/', include('allauth.urls')),
    #----------------------------Auuthentication------------------#
    path('register', views.Register.as_view(), name='register'),
    path('userlogin', views.UserLogin.as_view(), name='userlogin'),
    path('userlogout', views.Logout.as_view(), name='userlogout'),
    path('userChangePassword/<int:pk>', login_required(views.UserChangePassword.as_view()), name='userChangePassword'),
    #------------------------------Main Page----------------------#
    
    path('', login_required(views.Home.as_view()), name='home'),
    path('messages', login_required(views.Messages.as_view()), name='messages'),
    path('reels', login_required(views.Reels.as_view()), name='reels'),
    path('usersetting', login_required(views.UserSetting.as_view()), name='usersetting'),
    path("firebase-messaging-sw.js", views.ShowFireBaseJS.as_view(), name="show_firebase_js"),
    

    #-------------------------------Follow-UnFollow---------------------------------#
   

    #-------------------------------Post--------------------------------#
    
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
