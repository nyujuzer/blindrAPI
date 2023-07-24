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
from .views import register, login, get_hobbies, get_matches, finishSignUp, getFile, uploadVid, getAllVids, getThumbs
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('login/<str:email>+<str:password>/', login),
    path('finishSignup/', finishSignUp),
    path('getHobbies/', get_hobbies),
    path('getUsers/', get_matches),
    path('getFile/<str:uid>/', getFile),
    path('uploadVideo/', uploadVid),
    path('getThumbs/<str:uid>', getThumbs),
    path('videos/<str:uid>', getAllVids),
    #remove after testing
]
