from rest_framework import serializers

from location.models import CharacterPosition, Location
from characters.serializers import CharacterSerializer

class CharacterPositionSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    class Meta:
        model = CharacterPosition
        fields = ["id", "character", "location", "row", "column"]


class LocationSerializer(serializers.ModelSerializer):
    character_positions = CharacterPositionSerializer(many=True)
    class Meta:
        model = Location
        fields = "__all__"