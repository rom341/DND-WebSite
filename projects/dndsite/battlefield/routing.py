from django.urls import path

from battlefield.consumers import MoveCharacterConsumer

websocket_urlpatterns = [
    path("ws/battlefield/<int:current_lobby_id>/", MoveCharacterConsumer.as_asgi()),
]
