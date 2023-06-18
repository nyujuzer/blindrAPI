from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geoip2 import GeoIP2
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from .models import UserModel, DisplayModel, ImageModel, hobbiesModel
from .settings import MEDIA_ROOT, MEDIA_URL
from .globals import Globals
import uuid
from .regHelp import EmailIsAvailable
from .utils import get_geolocation
from.serializers import UserSerializer, displaySerializer, ImageModelSerializer, HobbySerializer
from rest_framework.decorators import api_view
import hashlib
from django.contrib.auth.hashers import make_password, check_password
from os import path


def is_email_in_use(email:str):
    # Check if email is already in use
    users = UserModel.objects.filter(email=email)
    return users.exists()


def process_data(data):
    processed_data = data
    processed_data["password"] = make_password(data["password"])
    processed_data['gender'] = Globals.Gender.Encode(data['gender'])
    processed_data['preferences'] = Globals.Gender.Encode(data['preferences'])
    processed_data['age'] = Globals.formatDate(data["age"].replace("-", "/"))
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

@csrf_exempt
def upload_image(request):
    print(request.POST)
    if request.method == 'POST' and request.FILES.get('image'):
        print("hello")
        image_file = request.FILES['image']
        # Handle the image file as needed (e.g., save it to a model, process it, etc.)
        # Example: Saving the image to a model
        image_model = ImageModel(image=image_file)
        print(image_file.is_valid())
        image_model.save()
        return JsonResponse({'success': True, 'message': 'Image uploaded successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Image upload failed'})
from django.http import JsonResponse

@api_view(["GET"])
def login(request, email, password):
    if is_email_in_use(email):
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

calls = 0
@api_view(['POST'])
def get_matches(request):
    print(request.data)
    user = DisplayModel.objects.filter(account = request.data['uid']).first()
    update_user(user, request.data['location'])    
    return JsonResponse({'users':'none yet'})

def update_user(user:DisplayModel, location):
    user.longitude = location['longitude']
    user.latitude = location['latitude']
    user.save()
    # user.update(longitude = location[0])
    # user.update(latitude = location[1])
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
