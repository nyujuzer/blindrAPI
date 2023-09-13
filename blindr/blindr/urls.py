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
from .views import register, login, finishSignUp, get_hobbies, get_matches, getProfileData, testNotif, uploadVid, getThumbs, getAllVids, update_user, get_random_videos, setLike, getLikes, getMessages
from django.urls import path
from django.conf import settings
from chat.routing import websocket_urlpatterns
from django.conf.urls.static import static


from django.conf import settings

# ... your normal urlpatterns here

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
path('setLikes/', setLike),
path('getLikes/<str:userId>/', getLikes),
path('getMessages/<str:userId>/<str:otherid>/', getMessages),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+websocket_urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)