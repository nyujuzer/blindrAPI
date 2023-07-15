from math import radians, sin, cos, sqrt, atan2
from django.contrib.gis.measure import Distance
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from requests import Response
from .models import UserModel, DisplayModel, ImageModel, hobbiesModel, VideoModel
from .settings import MEDIA_ROOT, MEDIA_URL
from .globals import Globals
import uuid
from .regHelp import EmailIsAvailable
from rest_framework.request import Request
from.serializers import UserSerializer, displaySerializer, ImageModelSerializer, VideoSerializer
from django.core.files.storage import FileSystemStorage

from rest_framework.decorators import api_view
import hashlib
from django.contrib.auth.hashers import make_password, check_password
from os import path


def is_email_in_use(email: str):
    # Check if email is already in use
    users = UserModel.objects.filter(email=email)
    return users.exists()


def process_data(data):
    processed_data = data
    processed_data["password"] = make_password(data["password"])
    processed_data['gender'] = int(Globals.Gender.Encode(data['gender']))
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
@api_view(['POST'])
def finishSignUp(request):      
    if request.method == 'POST':
        print(request.data)
        print(request.FILES)
        user :UserModel = UserModel.objects.get(userId=request.data['uid'])
        serializer = ImageModelSerializer(data={'user': user.userId, 'image': request.FILES.get("image"), 'isProfilePic': True}, context={'request': request, 'multipart': True})
        user.maxdist = int(request.data['maxDist'])
        user.save()
        user : DisplayModel= DisplayModel.objects.get(account = user)
        user.bio = request.data['bio']
        user.save()
        if serializer.is_valid():
            print("yay")
            serializer.save()
            return JsonResponse({'success': True, 'message': 'Image uploaded successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Image upload failed'})
@api_view(['POST'])
def uploadVid(request):
    print(request.data)
    user = UserModel.objects.get(userId=request.data['uid'])
    video = request.FILES['video']
    serializer = VideoSerializer(data={"user":user.userId, 'video':video, "title":"testing"}, context={'request': request, 'multipart': True})
    print(serializer.is_valid())
    instance = serializer.save()
    makeThumbnail(instance)
    return JsonResponse({"test":True})

def makeThumbnail(video:VideoModel):
    x = Globals.videoAdministration().generate_thumbnail(video.video.path,"test")
    print(x)
@api_view(['GET'])
def getVideo(request, uid):
    from wsgiref.util import FileWrapper
    user = UserModel.objects.get(userId=uid)

    video = VideoModel.objects.get(user = user)
    file = FileWrapper(open(video.video.path, 'rb'))
    response = HttpResponse(file, content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename=my_video.mp4'
    return response
def getAllVids(request, uid):
    try:
        user = UserModel.objects.get(userId=uid)
        file_obj = VideoModel.objects.get(user=user)
        print(file_obj, "this?")
    except VideoModel.DoesNotExist:
        print("404")
        return JsonResponse({"success": False, "reason": 'Not found'})
    
    # Retrieve the necessary video data
    video_data = {
        'video_path': file_obj.video.path,
        'title': file_obj.title,
    }

    return FileResponse(open(video_data['video_path'], 'rb'))   

@api_view(['GET'])
def getFile(request, uid):
    try:
        user = UserModel.objects.get(userId=uid)
        file_obj = ImageModel.objects.get(user=user)
        print(file_obj)
    except ImageModel.DoesNotExist:
        print("404")
        return JsonResponse({"success": False, "reason": 'Not found'})

    # Open and return the file as a response
    file = open(file_obj.image.path, 'rb')
    return FileResponse(file)

@api_view(["GET"])
def login(request, email, password):
    if is_email_in_use(email)==True:
        user = UserModel.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            response = JsonResponse({"login": "successful", 'uid': str(user.userId)})
            return response
        else:
            return JsonResponse({"login": "unsuccessful"})
    else:
        print(is_email_in_use(email))
        return JsonResponse({"login": "unsuccessful"})


@csrf_exempt
@api_view(["GET"])
def get_hobbies(request):
    hobbies = hobbiesModel.objects.all()
    data = {
        'hobbies': list(hobbies.values())
    }
    return JsonResponse(data)



@api_view(['POST'])
def get_matches(request):
    print(request.data)
    user_id = request.data['uid']
    user_longitude = float(request.data['location']['longitude'])
    user_latitude = float(request.data['location']['latitude'])

    # Get the user's display profile
    user = DisplayModel.objects.filter(account=user_id).first()
    if not user:
        return JsonResponse({'error': 'User not found'})

    # Update user's location
    user.longitude = user_longitude
    user.latitude = user_latitude
    user.save()

    # Filter potential matches based on gender preference
    potential_matches = DisplayModel.objects.filter(gender=user.preferences)

    # Calculate distances between user and potential matches
    matches = []
    for match in potential_matches:
        print(match)
        match_longitude = float(match.longitude)
        match_latitude = float(match.latitude)

        # Calculate distance using the Haversine formula
        R = 6371  # Radius of the Earth in kilometers
        dlon = radians(match_longitude - user_longitude)
        dlat = radians(match_latitude - user_latitude)
        a = sin(dlat / 2) ** 2 + cos(radians(user_latitude)) * cos(radians(match_latitude)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        if user.account.maxdist is None or distance < user.account.maxdist:
            matches.append(matches)
    print(matches)
    return JsonResponse({'matches': matches})

def update_user(user: DisplayModel, location):
    user.longitude = location['longitude']
    user.latitude = location['latitude']
    user.save()