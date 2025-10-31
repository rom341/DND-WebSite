from django.urls import path
from .consumers import BattlefieldConsumer

websocket_urlpatterns = [
    path("ws/battlefield/<group_name>", BattlefieldConsumer.as_asgi()),
]
