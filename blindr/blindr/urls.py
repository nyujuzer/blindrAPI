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
from .views import register, login, get_hobbies, get_matches, set_cookies , upload_image  
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('login/<str:email>+<str:password>/', login),
    path('uploadImage/', upload_image),
    path('getUsers/', get_matches),
    path('getHobbies/', get_hobbies),
    #remove after testing
    path('setCookies-<str:_name>+<str:_password>/', set_cookies),
    # path('uploadHobby', populateHobbies)
]
