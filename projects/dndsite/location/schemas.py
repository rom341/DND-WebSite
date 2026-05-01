from ninja import ModelSchema, Schema

from location.models import Location

class LocationSchema(ModelSchema):
    class Meta:
        model = Location
        fields = "__all__" 
        
class AddCharacterToLocationSchema(Schema):
    lobbyId: int
    characterId: int
    locationId: int
    targetRow: int
    targetColumn: int
        