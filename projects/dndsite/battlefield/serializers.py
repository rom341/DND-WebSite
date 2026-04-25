from rest_framework import serializers

from characters.serializers import CharacterPositionSerializer
from location.models import Location


class LocationSerializer(serializers.ModelSerializer):
    character_positions = CharacterPositionSerializer(many=True)
    class Meta:
        model = Location
        fields = "__all__"