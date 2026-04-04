from rest_framework import serializers

from battlefield.serializers import LocationSerializer
from lobby.models import Lobby

class LobbySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)
    class Meta:
        model = Lobby
        fields = "__all__"