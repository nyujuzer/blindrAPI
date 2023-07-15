from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from .globals import Globals

class hobbiesModel(models.Model):
    """
    Model representing hobbies.

    Attributes:
        hobby (str): The name of the hobby.

    Methods:
        __str__(): Returns the string representation of the hobby.
    """
    hobby = models.CharField(max_length=255)

    def __str__(self):
        return self.hobby


class UserModel(models.Model):
    """
    Model representing a user.

    Attributes:
        userId (UUIDField): The unique identifier for the user.
        password (str): The user's password.
        name (str): The name of the user.
        email (EmailField): The email address of the user.
        maxdist (IntegerField): The maximum distance for user preferences (nullable).

    Methods:
        __str__(): Returns the string representation of the user.
    """
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    maxdist = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class DisplayModel(models.Model):
    """
    Model representing the display information of a user.

    Attributes:
        account (ForeignKey): The associated user account.
        name (str): The display name.
        gender (IntegerField): The gender code (validated by MaxValueValidator).
        preferences (IntegerField): The preference code (validated by MaxValueValidator).
        hobbies (ManyToManyField): The hobbies associated with the user.
        bio (str): The user's bio.
        age (DateField): The user's age.
        longitude (str): The longitude coordinate (nullable).
        latitude (str): The latitude coordinate (nullable).

    Methods:
        __str__(): Returns the string representation of the display information.
    """
    account = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    gender = models.IntegerField(validators=[MaxValueValidator(3)])
    preferences = models.IntegerField(validators=[MaxValueValidator(4)])
    hobbies = models.ManyToManyField(hobbiesModel)
    bio = models.CharField(max_length=255)
    age = models.DateField()
    longitude = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - display. {Globals.Gender.Decode(self.gender)}'


class MatchesModel(models.Model):
    """
    Model representing user matches.

    Attributes:
        accountId (OneToOneField): The associated user account.
        matchesId (UUIDField): The unique identifier for the matches.
        matches (str): A string representing the matches.
        dislikes (str): A string representing the dislikes.
        likes (str): A string representing the likes.
    """
    accountId = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    matchesId = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    matches = models.CharField(max_length=2000)
    dislikes = models.CharField(max_length=20000)
    likes = models.CharField(max_length=20000)


class ImageModel(models.Model):
    """
    Model representing user images.

    Attributes:
        user (ForeignKey): The associated user.
        isProfilePic (BooleanField): Indicates if the image is a profile picture.
        image (ImageField): The user's image file.

    Methods:
        __str__(): Returns the string representation of the image.
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='images')
    isProfilePic = models.BooleanField()
    image = models.ImageField(upload_to="img")

    def __str__(self):
        return f'{self.image.name} - {self.user.name}'


class VideoModel(models.Model):
    """
    Model representing user videos.

    Attributes:
        user (ForeignKey): The associated user.
        video (FileField): The user's video file.
        title (str): The title of the video.

    Methods:
        __str__(): Returns the string representation of the video.
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to="videos", )
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title
class ThumbnailModel(models.Model):
    relatedvideo = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='related_video')
    thumbnail = models.ImageField(upload_to="thumbnails")
    def save(self, *args, **kwargs):
        if not self.thumbnail:
            video_path = self.relatedvideo.video.path
            thumbnail_path = f"thumbnails/{self.relatedvideo.title}.jpg"  # Customize the thumbnail filename if needed
            Globals.videoAdministration().generate_thumbnail(video_path, thumbnail_path)
            self.thumbnail.name = thumbnail_path
            super().save(*args, **kwargs)