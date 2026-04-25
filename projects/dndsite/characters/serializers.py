from rest_framework import serializers

from characters.models import Character, CharacterPosition, CharacterState

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["id", "user", "character_name", "entity_base", "level", "experience", "max_hit_points", "is_npc"]
        
class CharacterStateSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    class Meta:
        model = CharacterState
        fields = ["__all__"]
    

class CharacterPositionSerializer(serializers.ModelSerializer):
    character_state = CharacterStateSerializer()
    class Meta:
        model = CharacterPosition
        fields = ["id", "characterState", "location", "row", "column"]