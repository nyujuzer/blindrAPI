from math import radians, sin, cos, sqrt, atan2
from django.contrib.gis.measure import Distance
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from requests import Response, status_codes
from .models import UserModel, DisplayModel, ImageModel, hobbiesModel, VideoModel, ThumbnailModel
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


def is_email_in_use(email: str) -> bool:
    """
    Check if the given email is already in use by a user.

    Args:
        email (str): Email address to check.

    Returns:
        bool: True if the email is already in use, False otherwise.
    """
    users = UserModel.objects.filter(email=email)
    return users.exists()


def process_data(data: dict) -> dict:
    """
    Process the user registration data.

    Args:
        data (dict): User registration data.

    Returns:
        dict: Processed user registration data.
    """
    processed_data = data
    processed_data["password"] = make_password(data["password"])
    processed_data['gender'] = int(Globals.Gender.Encode(data['gender']))
    processed_data['preferences'] = Globals.Gender.Encode(data['preferences'])
    processed_data['age'] = Globals.formatDate(data["age"].replace("-", "/"))
    return processed_data


@api_view(['POST'])
def register(request: Request) -> JsonResponse:
    """
    Register a new user.

    This view handles the user registration process. It checks if the email is available,
    processes the registration data, and creates the user account and display information.

    Args:
        request (Request): Django REST Framework request object.

    Returns:
        JsonResponse: JSON response indicating the success status of the registration.
    """
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
def finishSignUp(request: Request) -> JsonResponse:
    """
    Finish the sign-up process.

    This view handles the completion of the sign-up process by saving the user's image, updating
    the user's maximum distance and bio, and returning a JSON response indicating the success status.

    Args:
        request (Request): Django REST Framework request object.

    Returns:
        JsonResponse: JSON response indicating the success status of the sign-up process.
    """
    if request.method == 'POST':
        user: UserModel = UserModel.objects.get(userId=request.data['uid'])
        serializer = ImageModelSerializer(data={'user': user.userId, 'image': request.FILES.get("image"), 'isProfilePic': True}, context={'request': request, 'multipart': True})
        user.maxdist = int(request.data['maxDist'])
        user.save()
        user: DisplayModel = DisplayModel.objects.get(account=user)
        user.bio = request.data['bio']
        user.save()
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'message': 'Image uploaded successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Image upload failed'})


@api_view(['POST'])
def uploadVid(request: Request) -> JsonResponse:
    """
    Upload a video for a user.

    This view handles the video upload process. It receives the video file and user ID,
    saves the video file, creates a VideoModel object, and returns a JSON response.

    Args:
        request (Request): Django REST Framework request object.

    Returns:
        JsonResponse: JSON response indicating the success status of the video upload.
    """
    user = UserModel.objects.get(userId=request.data['uid'])
    video = request.FILES['video']
    serializer = VideoSerializer(data={"user": user.userId, 'video': video, "title": "testing"}, context={'request': request, 'multipart': True})
    if serializer.is_valid():
        instance = serializer.save()
        print(type(instance))
        makeThumbnail(instance, user)
        return JsonResponse({"success": True})
    else: 
        print(serializer.errors)
        return JsonResponse({"success": False})

def makeThumbnail(video: VideoModel, user):
    """
    Create a thumbnail for a video.

    This function generates a thumbnail image for the given video using a custom method.
    It saves the thumbnail image and associates it with the video.

    Args:
        video (VideoModel): The video model object for which the thumbnail is being generated.
    """
    print(video.video)
    x = Globals.generate_thumbnail(video.video.path , video, user)


@api_view(['GET'])
def getVideo(request: Request, uid: str) -> HttpResponse:
    """
    Get the video file for a user.

    This view retrieves the video file associated with the given user ID and returns it as a response.

    Args:
        request (Request): Django REST Framework request object.
        uid (str): User ID.

    Returns:
        HttpResponse: HTTP response containing the video file.
    """
    from wsgiref.util import FileWrapper
    user = UserModel.objects.get(userId=uid)

    video = VideoModel.objects.get(user=user)
    file = FileWrapper(open(video.video.path, 'rb'))
    response = HttpResponse(file, content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename=my_video.mp4'
    return response


def getAllVids(request: Request, uid: str) -> JsonResponse:
    """
    Get all video files for a user.

    This view retrieves all video files associated with the given user ID and returns them as a response.

    Args:
        request (Request): Django REST Framework request object.
        uid (str): User ID.

    Returns:
        JsonResponse: JSON response containing the video files.
    """
    try:
        user = UserModel.objects.get(userId=uid)
        file_obj = VideoModel.objects.get(user=user)
        print(file_obj, "this?")
    except VideoModel.DoesNotExist:
        print(print(VideoModel.DoesNotExist))
        return JsonResponse({"success": False, "reason": 'Not found'})

    # Retrieve the necessary video data
    video_data = {
        'video_path': file_obj.video.path,
        'title': file_obj.title,
    }

    return FileResponse(open(video_data['video_path'], 'rb'))

@api_view(['GET'])
def getThumbs(request, uid):
    user = UserModel.objects.get(userId=uid)
    print(user)
    thumbnail = ThumbnailModel.objects.all().filter(user=user)
    print(thumbnail)
    return JsonResponse({"testing":True})
@api_view(['GET'])
def getFile(request: Request, uid: str) -> FileResponse:
    """
    Get the image file for a user.

    This view retrieves the image file associated with the given user ID and returns it as a response.

    Args:
        request (Request): Django REST Framework request object.
        uid (str): User ID.

    Returns:
        FileResponse: HTTP response containing the image file.
    """
    try:
        user = UserModel.objects.get(userId=uid)
        file_obj = ImageModel.objects.get(user=user)
        print(file_obj)
    except ImageModel.DoesNotExist:
        print("404")
        response = FileResponse()
        response.status_code = 404
        return response

    # Open and return the file as a response
    file = open(file_obj.image.path, 'rb')
    print(file)
    response = FileResponse(file)
    response.status_code = 200
    return response


@api_view(["GET"])
def login(request: Request, email: str, password: str) -> JsonResponse:
    """
    User login.

    This view handles the user login process. It checks if the email and password are correct
    and returns a JSON response indicating the success status of the login process.

    Args:
        request (Request): Django REST Framework request object.
        email (str): User's email address.
        password (str): User's password.

    Returns:
        JsonResponse: JSON response indicating the success status of the login process.
    """
    if is_email_in_use(email) == True:
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
def get_hobbies(request: Request) -> JsonResponse:
    """
    Get the list of hobbies.

    This view retrieves the list of hobbies and returns them as a JSON response.

    Args:
        request (Request): Django REST Framework request object.

    Returns:
        JsonResponse: JSON response containing the list of hobbies.
    """
    hobbies = hobbiesModel.objects.all()
    data = {
        'hobbies': list(hobbies.values())
    }
    return JsonResponse(data)


@api_view(['POST'])
def get_matches(request: Request) -> JsonResponse:
    """
    Get matching users.

    This view retrieves the matching users based on the user's preferences and location.
    It calculates the distances between the users and filters potential matches based on
    the maximum distance set by the user.

    Args:
        request (Request): Django REST Framework request object.

    Returns:
        JsonResponse: JSON response containing the matching users.
    """
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
        match_longitude = float(match.longitude)
        match_latitude = float(match.latitude)

        # Calculate distance using the Haversine formula
        R = 6371  # Radius of the Earth in kilometers
        dlon = radians(match_longitude - user_longitude)
        dlat = radians(match_latitude - user_latitude)
        a = sin(dlat / 2) ** 2 + cos(radians(user_latitude)) * cos(radians(match_latitude)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        # Filter matches based on maximum distance
        if user.account.maxdist is None or distance < user.account.maxdist:
            matches.append(matches)

    return JsonResponse({'matches': matches})


def update_user(user: DisplayModel, location: dict):
    """
    Update the user's location.

    This helper function updates the user's longitude and latitude coordinates based on the provided location.

    Args:
        user (DisplayModel): The user's display model object.
        location (dict): Dictionary containing the user's location coordinates.
    """
    user.longitude = location['longitude']
    user.latitude = location['latitude']
    user.save()
