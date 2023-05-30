from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from .models import UserModel, DisplayModel, ImageModel, hobbiesModel
from .settings import MEDIA_ROOT, MEDIA_URL
from .globals import Globals
import uuid
from .regHelp import EmailIsAvailable
from.serializers import UserSerializer, displaySerializer, ImageModelSerializer, HobbySerializer
from rest_framework.decorators import api_view
import hashlib
from django.contrib.auth.hashers import make_password, check_password
from os import path


def is_email_in_use(email:str):
    # Check if email is already in use
    users = UserModel.objects.filter(email=email.lower())
    return users.exists()


def process_data(data):
    processed_data = data
    processed_data["password"] = make_password(data["password"])
    processed_data['gender'] = Globals.Gender.Encode(data['gender'])
    processed_data['preferences'] = Globals.Gender.Encode(data['preferences'])
    processed_data['age'] = Globals.formatDate(data["age"])
    return processed_data


@api_view(['POST'])
def register(request):
    if not is_email_in_use(request.data['email']):
        data = process_data(request.data)
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            data['account'] = user.userId
            display_serializer = displaySerializer(data=data)
            if display_serializer.is_valid():
                display_serializer.save()
                return JsonResponse({"success": True})
            else:
                print(display_serializer.errors)
                print(request.data['hobbies'])
                user.delete()
                return JsonResponse({"success": False})
        else:
            return JsonResponse({"success": False})

    return JsonResponse({"success": False, "error": "all"})


def upload_image(request):
    if request.method == "POST":
        image_serializer = ImageModelSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.validated_data.get('image')
            image_serializer.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse(image_serializer.errors)

    return JsonResponse({"message": "This is a GET request"})

from django.http import JsonResponse

@api_view(["GET"])
def login(request, email, password):
    if is_email_in_use(email.lower()):
        user = UserModel.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            response = JsonResponse({"login": "successful", 'uid': str(user.userId)})
            print(response.cookies)
            return response
        else:
            return JsonResponse({"login": "unsuccessful"})
    else:
        print(is_email_in_use(email))
        return JsonResponse({"login":"unsuccessful"})



def get_hobbies(request):
    hobbies = hobbiesModel.objects.all()
    data = {
        'hobbies': list(hobbies.values())
    }
    return JsonResponse(data)


def get_matches(request):
    user = UserModel.objects.filter(email=request.data)
    # Further implementation


def set_cookies(request, name, password):
    user = UserModel.objects.all().filter(name=name)
    request.session['name'] = name
    request.session['pass'] = hashlib.sha256(password.encode("utf-8")).hexdigest()
    request.session['uid'] = str(user[0].userId)
    return JsonResponse({"test": "0"})


@api_view(["GET", "POST"])
def video_upload(request):
    # Placeholder, further implementation required
    return JsonResponse("")
