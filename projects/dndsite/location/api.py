from ninja import NinjaAPI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.db import transaction

from characters.models import Character
from characters.schemas import CharacterPositionSchema
from location.models import Location
from lobby.models import Lobby, LobbyRole
from location.schemas import AddCharacterToLocationSchema, LocationSchema
from service.lobby_services import add_character_to_lobby
from service.location_services import add_character_to_location
from service.role_services import get_gm_role
from django.shortcuts import get_object_or_404

app = NinjaAPI()

@app.post("location/add_character_to_location", response=CharacterPositionSchema)
def add_character(request, addCharacterToLocationSchema: AddCharacterToLocationSchema):
    data = addCharacterToLocationSchema.model_dump()
    lobby = get_object_or_404(Lobby, id=data.get("lobbyId"))
    active_user = request.user        
    if not LobbyRole.objects.user_has_role(active_user, lobby, get_gm_role()):
        return Response("Has no GM role", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    character = get_object_or_404(Character, id=data.get("characterId"))
    location = get_object_or_404(Location, id=data.get("locationId"))
    target_row = data.get("targetRow")
    target_column = data.get("targetColumn")
    
    with transaction.atomic():  
        new_character_state = add_character_to_lobby(character=character, lobby=lobby)
        character_position = add_character_to_location(character_state=new_character_state, location=location, target_row=target_row, target_column=target_column)
    return character_position
