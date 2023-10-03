from django.urls import re_path

from . import consumers

channel_routing = {
    'websocket.connect': consumers.ChatConsumer.connect,
    'websocket.receive': consumers.ChatConsumer.receive,
    'websocket.disconnect': consumers.ChatConsumer.disconnect,
}

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]