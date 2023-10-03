from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/test/', consumers.ChatConsumer.as_asgi()),
]