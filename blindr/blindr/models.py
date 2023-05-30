from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from os.path import join
from.settings import MEDIA_URL


class hobbiesModel(models.Model):
    id = models.IntegerField(primary_key=True)
    hobby = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.hobby}'
class UserModel(models.Model):
    """
    userId:the id of the user, private
    password: the password of the user, charfield
    name: the name of the user, charfield
    """
    userId=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    def __str__(self):
        return f'{self.name}'
    
class DisplayModel(models.Model):
    """
    accountid: the id of the private account
    name: the name displayed when shown
    gender: a dictionary of 5 items - male, female, non-binary other
    preferences: dictionary of 4 items - female, male, does not matter 
    hobbies: a ';' divided list
    """
    account = models.OneToOneField(UserModel, on_delete=models.CASCADE, )
    name=models.CharField(max_length=255)
    gender = models.IntegerField(validators=[MaxValueValidator(3)])
    preferences = models.IntegerField(validators=[MaxValueValidator(4)])
    hobbies = models.ManyToManyField(hobbiesModel)
    age = models.DateField()

    def __str__(self) -> str:
        return f'{self.name} - display'
class MatchesModel(models.Model): 
    accountId= models.OneToOneField(UserModel, on_delete=models.CASCADE)
    matchesId = models.UUIDField (default=uuid.uuid4, primary_key=True, editable=False)
    matches = models.CharField(max_length=2000)
    dislikes = models.CharField(max_length=20000)
    likes = models.CharField(max_length=20000)

class ImageModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    isProfileImage = models.BooleanField()
    image = models.ImageField(upload_to="img")
    def __str__(self) -> str:
        return self.image.name+"-"+self.user.name
class VideoModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    video = models.FileField(upload_to="img/%y")
    title = models.CharField(max_length=30)
    def __str__(self):
        return f'{self.title}'
    