from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

from core.managers.SessionManager import SessionManager
from location.models import Location
from battlefield.serializers import LocationSerializer
from lobby.models import Lobby, LobbyRole
from lobby.serializers import LobbySerializer
from service.lobby.actions import add_user_as_player_to_lobby
from service.role.selectors import get_gm_role

class LobbyApi(APIView):
    @api_view(('GET',))
    def get_locations_for_lobby(request, lobby_id=None) -> Response:
        if not lobby_id:
            return Response("Not valid ID", status=status.HTTP_400_BAD_REQUEST)
        
        locations = Location.objects.get_locations_for_lobby_by_id(lobby_id=lobby_id)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(('GET',))
    def get_lobby(request, lobby_id=None) -> Response:
        if not lobby_id:
            return Response("Not valid ID", status=status.HTTP_400_BAD_REQUEST)
        
        lobby = Lobby.objects.get_lobby_by_id(lobby_id=lobby_id)
        serializer = LobbySerializer(lobby)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(('POST',))
    def add_user_to_lobby(request):
        if request.method != 'POST':
            return Response("Not valid method", status=status.HTTP_400_BAD_REQUEST)

        lobby_id = request.data.get('lobbyId')
        lobby = Lobby.objects.get_lobby_by_id(lobby_id=lobby_id)
        selected_user_id = request.data.get('selectedUserId')
        selected_user = User.objects.get(id=selected_user_id)
        active_user = request.user
        
        
        if not LobbyRole.objects.user_has_role(active_user, lobby, get_gm_role()):
            return Response("Has no GM role", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        add_user_as_player_to_lobby(user=selected_user, lobby=lobby)
        return Response(status=status.HTTP_200_OK)
