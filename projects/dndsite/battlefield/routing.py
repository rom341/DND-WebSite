from django.urls import path
from .consumers import MoveCharacterConsumer

websocket_urlpatterns = [
    path("ws/battle/<int:group_id>/", MoveCharacterConsumer.as_asgi()),
]
