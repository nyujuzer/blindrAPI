from math import radians, sin, cos, sqrt, atan2
from time import sleep
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from .utils import stream
from django.db.models import Q
from .utils import calculate_distance
from .models import UserModel, DisplayModel, ImageModel, Message,hobbiesModel, VideoModel, ThumbnailModel, MatchesModel
from .settings import MEDIA_ROOT, MEDIA_URL
from .globals import Globals
from wsgiref.util import FileWrapper
from.serializers import UserSerializer, displaySerializer, ImageModelSerializer, VideoSerializer, ThumbnailSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from os import path

stream = stream()

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
def register(request) -> JsonResponse:
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
def finishSignUp(request) -> JsonResponse:
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
            print(request.FILES)
            return JsonResponse({'success': False, 'message': 'Image upload failed'})


@api_view(['POST'])
def uploadVid(request) -> JsonResponse:
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
    print(len(request.data['title']))
    serializer = VideoSerializer(data={"user": user.userId, 'video': video, "title": request.data['title']}, context={'request': request, 'multipart': True})
    if serializer.is_valid():
        instance = serializer.save()
       # makeThumbnail(instance, user)
        print("Waiting")

        return JsonResponse({"success": True})
    else: 
        if 'title' in serializer.errors.keys():
            return JsonResponse({'success':False, "reason":"tooShort"})
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
def getVideo(request, uid: str) -> HttpResponse:
    """
    Get the video file for a user.

    This view retrieves the video file associated with the given user ID and returns it as a response.

    Args:
        request (Request): Django REST Framework request object.
        uid (str): User ID.

    Returns:
        HttpResponse: HTTP response containing the video file.
    """
    user = UserModel.objects.get(userId=uid)

    video = VideoModel.objects.get(user=user)
    file = FileWrapper(open(video.video.path, 'rb'))
    response = HttpResponse(file, content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename=my_video.mp4'
    return response


def getAllVids(request, uid: str) -> JsonResponse:
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
        file_obj = VideoModel.objects.all().filter(user=user)
    except VideoModel.DoesNotExist:
        print(print(VideoModel.DoesNotExist))
        return JsonResponse({"success": False, "reason": 'Not found'})

    retlist = []
    # Retrieve the necessary video data
    for video in file_obj:

        video_data = {
            'title': video.title,
            'video_url': video.video.url,
            'pk': video.pk
        }
        retlist.append(video_data)
    """    title:string,
    video_url:string,
    pk:string,
    thumbnail_url?:string,"""
    print(video_data)
    return JsonResponse(retlist, safe=False)    

@api_view(['GET'])
def getThumbs(request, uid):


    # Get the current user from the request (assuming you're using some form of authentication)
    current_user = UserModel.objects.get(userId=uid)  # Adjust this line based on your authentication method

    # Query ThumbnailModel objects for the current user and select the related Video object
    thumbnail_list = ThumbnailModel.objects.filter(user=current_user).select_related('relatedvideo').all()

    # Create a list to store the serialized data
    serialized_list = []

    # Serialize each object to a dictionary and add it to the list
    for thumbnail in thumbnail_list:
        serialized_thumbnail = {
            'title': thumbnail.relatedvideo.title,
            'video_url': thumbnail.relatedvideo.video.url,
            'thumbnail_url': thumbnail.thumbnail.url,
            # Add other fields from ThumbnailModel if needed
        }
        serialized_list.append(serialized_thumbnail)

    # Return the serialized list as JSON response
    print(serialized_list)
    return JsonResponse(serialized_list, safe=False)


@api_view(['GET'])
def getProfileData(request, uid: str, ) -> JsonResponse:
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
        returnData = {'success':True,'username':DisplayModel.objects.get(account_id=user).name, 'profileImageRoute':file_obj.image.url}
    except ImageModel.DoesNotExist:
        response = JsonResponse({"success":False, "reason":"CantFindImage"})
        return response

    # Open and return the file as a response
    file = open(file_obj.image.path, 'rb')
    print(file)
    response = JsonResponse(returnData)
    response.status_code = 200
    return response

import random


@api_view(["GET"])
def get_random_videos(request, uid, amount, pks:str=''):
    # Step 1: Retrieve the current user from the request
    current_user = UserModel.objects.get(userId = uid)
    current_user_display = DisplayModel.objects.get(account = current_user)
    pks = pks.split("-")
    # Step 2: Get the current user's latitude and longitude (if available)
    user_latitude = None
    user_longitude = None
    if current_user_display.latitude and current_user_display.longitude:
        user_latitude = float(current_user_display.latitude)
        user_longitude = float(current_user_display.longitude)

    # Step 3: Get the max distance for user preferences (if available)
    max_distance = current_user.maxdist

    # Step 4: Filter the VideoModel objects associated with the current user
    videos = VideoModel.objects.exclude(user=current_user)
    print(videos)

    # Step 5: Randomize the order of the videos
    randomized_videos = list(videos)
    random.shuffle(randomized_videos)

    # Step 6: Check if the uploader of each video is within the user's maxdist (if available)
    nearby_videos = []
    for video in randomized_videos:
        uploader = DisplayModel.objects.get(account = video.user)
        if user_latitude and user_longitude and max_distance:
            uploader_latitude = float(uploader.latitude)
            uploader_longitude = float(uploader.longitude)
            distance = calculate_distance(user_latitude, user_longitude, uploader_latitude, uploader_longitude)
            if distance <= max_distance and str(video.pk) not in pks and userGenderComp(DisplayModel.objects.all().get(account=video.user), current_user_display):
                nearby_videos.append(video)
        else:
            nearby_videos.append(video)

    # Step 7: Return the list of nearby videos as a JSON response
    video_list = []
    for video in nearby_videos:
        video_info = {
            'pk':video.pk,
            'title': video.title,
            'video_url': video.video.url,
            # Add any other video information you want to include in the response
        }
        video_list.append(video_info)
    print(video_list[0:amount])
    return JsonResponse({'videos': video_list[0:amount]})
def userGenderComp(slave:DisplayModel, master:DisplayModel) ->bool:
    """
    goalDef : 
    To return a boolean if the users are compatible by gender and preferences
    guidelines:
        unless preferences are any: only return true if the user preferences and the other user's gender is the same
        if any, return true anyways
    """
    # print(slave, master)
    ret = False
    if Globals.Gender.Decode(master.preferences) == "ANY":
        ret = True
    elif master.preferences == slave.gender:
        ret = True
    # print(ret)
    return ret
@api_view(["GET"])
def login(request, email: str, password: str) -> JsonResponse:
    # import lzma
    # from importlib.metadata import version
    # print(version('lzma'))
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
def get_hobbies(request) -> JsonResponse:
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
def get_matches(request) -> JsonResponse:
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
def checkLikes(user1:DisplayModel, user2:UserModel):
    user1_usermodel = user1.account
    user2_displaymodel = DisplayModel.objects.get(account = user2)
    if user2.currentLikes.contains(user1) and user1_usermodel.currentLikes.contains(user2_displaymodel):
        test = MatchesModel.objects.create(user_1=user1_usermodel, user_2=user2)
    else:
        print("nah")
@api_view(['POST'])
def setLike(request):
    pk = request.data['video']
    print(pk)
    video = VideoModel.objects.get(pk = int(pk))
    liked_user = DisplayModel.objects.get(account = video.user)
    liking_user = UserModel.objects.get(userId = request.data['uid'])
    liking_user.currentLikes.add(liked_user)
    checkLikes(liked_user, liking_user)
    return JsonResponse({'test':True})
@csrf_exempt
@api_view(['POST'])
def update_user(request):
    """
    Update the user's location.

    This helper function updates the user's longitude and latitude coordinates based on the provided location.

    Args:
        user (DisplayModel): The user's display model object.
        location (dict): Dictionary containing the user's location coordinates.
    """
    uid = request.data['uid']
    print(request.data)
    user = DisplayModel.objects.filter(account=UserModel.objects.get(userId=uid))[0]
    location = request.data['location']
    user.longitude = location['longitude']
    user.latitude = location['latitude']
    user.save()
    return JsonResponse({"Success":True})

@api_view(['GET'])
def getLikes(request, userId):
    # print(UserModel.objects.get(name = "testgirl").userId)
    user = UserModel.objects.get(userId = userId)
    matches = MatchesModel.objects.filter(user_1 = user) | MatchesModel.objects.filter(user_2 = user)
    serialized_data = []
    for match in matches:
        if str(match.user_1.userId) == userId:#if user1's userid isn't the passed in userid
            image = ImageModel.objects.get(user = match.user_2)
            print(user,"u2", match.user_2)
        elif str(match.user_2.userId) == userId:
            image = ImageModel.objects.get(user = match.user_1)
            print(user, "u1", match.user_1)
        data ={
            "id":image.user.userId,
                "pfpurl":image.image.url,
    "profileName":image.user.name,
    "lastText":Message.objects.filter(match=match).last().content if Message.objects.filter(match=match).last() else None
        }
        serialized_data.append(data)
    return JsonResponse({"results":serialized_data})

@api_view(['GET'])
def getMessages(request, userId, otherid):
    match = MatchesModel.objects.get(
                Q(user_1=userId, user_2=otherid) |
                Q(user_1=otherid, user_2=userId)
            )
    messages = Message.objects.filter(match = match).order_by('timestamp').reverse()
    messages = [i.to_gifted_chat_message() for i in messages]
    # messages.reverse()
    return JsonResponse({"data":messages})

def testNotif(request):
    return(JsonResponse({"hekki":True}))