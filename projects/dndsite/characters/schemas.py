from ninja import ModelSchema

from characters.models import Character, CharacterPosition, CharacterState, EntityBase
from lobby.schemas import LobbySchema
from location.schemas import LocationSchema

class EntityBaseSchema(ModelSchema):
    class Meta:
        model = EntityBase
        fields = "__all__"

class CharacterSchema(ModelSchema):
    entity_base: EntityBaseSchema | None = None
    class Meta:
        model = Character
        fields = "__all__"
        
class CharacterStateSchema(ModelSchema):
    character: CharacterSchema | None = None
    lobby: LobbySchema | None = None
    class Meta:
        model = CharacterState
        fields = "__all__"
        

class CharacterPositionSchema(ModelSchema):
    character_state: CharacterStateSchema | None = None
    location: LocationSchema 
    class Meta:
        model = CharacterPosition
        fields = "__all__"