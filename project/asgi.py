import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import translator.routing
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
channel_layer = channels.asgi.get_channel_layer()

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            translator.routing.websocket_urlpatterns
        )
    ),
})
