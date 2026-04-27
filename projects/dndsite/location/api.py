from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.db import transaction

from characters.models import Character
from location.models import Location
from lobby.models import Lobby, LobbyRole
from service.lobby_services import add_character_to_lobby
from service.location_services import add_character_to_location
from service.role_services import get_gm_role

class LocationApi(APIView):
    @api_view(('POST',))
    def add_character_to_location(request):
        if request.method != 'POST':
            return Response("Not valid method", status=status.HTTP_400_BAD_REQUEST)

        lobby_id = request.data.get('lobbyId')
        lobby = Lobby.objects.get_lobby_by_id(lobby_id=lobby_id)
        active_user = request.user        
        if not LobbyRole.objects.user_has_role(active_user, lobby, get_gm_role()):
            return Response("Has no GM role", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        
        selected_character_id = request.data.get('characterId')
        selected_character = Character.objects.get_character_by_id(character_id=selected_character_id)
        selected_location_id = request.data.get('locationId')
        selected_location = Location.objects.get_location_by_id(location_id=selected_location_id) 
        target_row = request.data.get('targetRow')
        target_column = request.data.get('targetColumn')
        
        with transaction.atomic():            
            new_character_state = add_character_to_lobby(character=selected_character, lobby=lobby)
            add_character_to_location(character_state=new_character_state, location=selected_location, target_row=target_row, target_column=target_column)
        return Response(status=status.HTTP_200_OK)
