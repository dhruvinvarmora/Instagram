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
from post import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required 
from django.conf import settings
from django.conf.urls.static import static
app_name="post"


urlpatterns = [
     path('createpost', views.CreatePostView.as_view(), name='createpost'),
     path('postdetail/<int:pk>', views.PostDetail.as_view(), name='postdetail'),
     path('postdelete/<int:pk>', views.PostDeleteView.as_view(), name='postdelete'),
     path('like', views.LikeView.as_view(), name='like'),
     path('createcomment', views.CreateCommentView.as_view(), name='createcomment'),
     path('AddArchive', views.PostAddtoFavoriteView.as_view(), name='AddArchive'),
     path('showArchive', views.ShowArchive.as_view(), name='showArchive'),
     
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
