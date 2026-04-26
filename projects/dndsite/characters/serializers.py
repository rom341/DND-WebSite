from rest_framework import serializers

from characters.models import Character, CharacterPosition, CharacterState

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"
        
class CharacterStateSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    class Meta:
        model = CharacterState
        fields = "__all__"
    

class CharacterPositionSerializer(serializers.ModelSerializer):
    character_state = CharacterStateSerializer()
    class Meta:
        model = CharacterPosition
        fields = "__all__"