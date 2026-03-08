from rest_framework import serializers

from battlefield.models import CharacterPosition

class CharacterPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterPosition
        fields = ["id", "character", "location", "row", "column"]