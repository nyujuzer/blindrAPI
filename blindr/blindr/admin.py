from django.contrib import admin
from .models import UserModel, DisplayModel, ImageModel, hobbiesModel

admin.site.register(UserModel)
admin.site.register(DisplayModel)
admin.site.register(ImageModel)
admin.site.register(hobbiesModel)