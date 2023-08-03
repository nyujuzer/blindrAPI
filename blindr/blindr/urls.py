"""blindr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from .views import register, login, get_hobbies, get_matches, finishSignUp, getProfileData, uploadVid, getAllVids, getThumbs, update_user, get_random_videos, setLike
from django.urls import path
from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('login/<str:email>+<str:password>/', login),
    path('finishSignup/', finishSignUp),
    path('getHobbies/', get_hobbies),
    path('getUsers/', get_matches),
    path('getProfileData/<str:uid>/', getProfileData),
    path('uploadVideo/', uploadVid),
    path('getThumbs/<str:uid>', getThumbs),
    path('videos/<str:uid>', getAllVids),
    path('updateLocation/', update_user),
    path('getRandomVideos/<str:uid>/<int:amount>/<str:pks>', get_random_videos),
    path('getRandomVideos/<str:uid>/<int:amount>/', get_random_videos),
    path('setLikes/', setLike)
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
