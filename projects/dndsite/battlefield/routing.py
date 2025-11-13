from django.urls import path
from .consumers import MoveCharacterConsumer

websocket_urlpatterns = [
    path("ws/battlefield/<int:current_group_id>/", MoveCharacterConsumer.as_asgi()),
]
