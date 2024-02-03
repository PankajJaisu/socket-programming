
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path 
from core.consumers import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
django.setup() 

django_application = get_asgi_application()


ws_patterns = [
    # path('ws/chat/',TestConsumer.as_asgi())
    path('chat/<room_code>',ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
    'websocket':URLRouter(ws_patterns)
    }
)


