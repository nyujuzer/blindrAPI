from django.db import models
# from .fields import messageField
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import datetime
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
        maxAge (IntegerField): The maximum distance for user preferences (nullable).

        
    Methods:
        __str__(): Returns the string representation of the user.
    """
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    maxdist = models.IntegerField(null=True, blank=True)
    maxAge = models.IntegerField(null=True, blank=True)
    currentLikes = models.ManyToManyField('DisplayModel', blank=True)


    def __str__(self):
        return f"{self.name}-ACCOUNT"


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

    def getAgeInYear(self)->int:
        birthdate = self.age
        year, month, day = map(int, str(birthdate).split("-"))
        today = datetime.date.today()
        age = today.year - year - ((today.month, today.day) < (month, day))
        return age
    def __str__(self):
        return f'{self.name}-DISPLAY: {Globals.Gender.Decode(self.gender)} x {Globals.Gender.Decode(self.preferences)}'


class MatchesModel(models.Model):
    """
    user_1: usermodel
    user_2: usermodel
    ephemeral: boolean
    """
    user_1 = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="one")
    user_2 = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="two")
    ephemeral = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user_1} and {self.user_2}'

class Message(models.Model):
    match = models.ForeignKey(MatchesModel, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def to_gifted_chat_message(self):
        """
        Converts the Django Message model to Gifted Chat's message format.
        """
        return {
            '_id': self.id,
            'text': self.content,
            'createdAt': self.timestamp.isoformat(),  # Convert datetime to string
            'user': {
                '_id': str(self.sender.userId),
                'name': self.sender.name,
            },
        }

    def __str__(self):
        return f'{self.sender} to {self.match}, cont = {self.content}'


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
        return f'{self.image} - {self.user.name}'


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
    video = models.FileField(upload_to="videos")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="NULL")
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}-{self.user}"


class ThumbnailModel(models.Model):
    """
    Model representing thumbnails for user videos.

    Attributes:
        relatedvideo (ForeignKey): The associated video.
        thumbnail (ImageField): The thumbnail image.

    Methods:
        save(): Overrides the default save() method to generate and save the thumbnail automatically.
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user")
    relatedvideo = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='related_video')
    thumbnail = models.ImageField(upload_to="thumbnails")

    def save(self, *args, **kwargs):
        """
        Overrides the default save() method to generate and save the thumbnail automatically.
        The thumbnail is generated using the associated video and saved to the 'thumbnails' directory.
        """
        if not self.thumbnail:
            video_path = self.relatedvideo.video.path
            thumbnail_path = f"thumbnails/{self.relatedvideo.title}.jpg"  # Customize the thumbnail filename if needed
            Globals.generate_thumbnail(video_path, thumbnail_path)  # Assuming there's a method to generate thumbnails
            self.thumbnail.name = thumbnail_path
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Thumbnail for {self.relatedvideo.title}'

class likes(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="liker")
    tags = models.JSONField()

"""
User metrics to track:

    Likes, tags

    tags->taken from description
    likes->self explainatory.

possible db models:
    likes(user, videopk, tags{possibly a dict?})
"""