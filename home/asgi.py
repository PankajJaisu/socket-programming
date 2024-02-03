import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack
from django.urls import path
from core.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
django.setup()

django_application = get_asgi_application()

ws_patterns = [
    path('chat/<room_code>', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_application,  # Add the Django application for HTTP
    "websocket": AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            URLRouter(ws_patterns)
        )
    ),
})
