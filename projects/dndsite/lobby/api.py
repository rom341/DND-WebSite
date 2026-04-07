from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from battlefield.models import Location
from battlefield.serializers import LocationSerializer
from lobby.models import Lobby
from lobby.serializers import LobbySerializer

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