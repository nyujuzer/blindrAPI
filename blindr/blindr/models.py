from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from .globals import Globals
class hobbiesModel(models.Model):
    hobby = models.CharField(max_length=255)

    def __str__(self):
        return self.hobby


class UserModel(models.Model):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    maxdist = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class DisplayModel(models.Model):
    account = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    gender = models.IntegerField(validators=[MaxValueValidator(3)])
    preferences = models.IntegerField(validators=[MaxValueValidator(4)])
    hobbies = models.ManyToManyField(hobbiesModel)
    bio = models.CharField(max_length=500)
    age = models.DateField()
    longitude = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - display . {Globals.Gender.Decode(self.gender)}'


class MatchesModel(models.Model):
    accountId = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    matchesId = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    matches = models.CharField(max_length=2000)
    dislikes = models.CharField(max_length=20000)
    likes = models.CharField(max_length=20000)


class ImageModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='images')
    isProfileImage = models.BooleanField()
    image = models.ImageField(upload_to="img")

    def __str__(self):
        return f'{self.image.name} - {self.user.name}'


class VideoModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to="img/%y")
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title
