from rest_framework import serializers
from .models import UserModel, DisplayModel, ImageModel, hobbiesModel, VideoModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [ 'name', 'password', 'email']
class displaySerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplayModel
        fields = ["account",'name', 'gender','preferences', 'hobbies', 'age', 'longitude', 'latitude']
class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['user','image', "isProfilePic"]
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields = ["user", 'video', 'title']
class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = hobbiesModel
        fields = ['id', 'hobby']