from django.contrib import admin
from .models import UserModel,Message, DisplayModel, ImageModel, hobbiesModel, VideoModel, ThumbnailModel, MatchesModel

admin.site.register(UserModel)
admin.site.register(DisplayModel)
admin.site.register(ImageModel)
admin.site.register(hobbiesModel)
admin.site.register(VideoModel)
admin.site.register(ThumbnailModel)
admin.site.register(MatchesModel)
admin.site.register(Message)