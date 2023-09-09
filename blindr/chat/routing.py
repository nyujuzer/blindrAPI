from django.urls import path
from . import consumers
from django.conf.urls.static import static

from blindr.settings import MEDIA_ROOT, MEDIA_URL

websocket_urlpatterns = [
    path('ws/<str:username>/<str:recipient_username>/', consumers.ChatConsumer.as_asgi()),
]