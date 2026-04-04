from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from battlefield.models import CharacterPosition, Location
from battlefield.serializers import CharacterPositionSerializer, LocationSerializer
from lobby.models import Lobby
from lobby.serializers import LobbySerializer

class CharacterPositionApi(APIView):
    def get(self, request) -> Response:
        character_positions = CharacterPosition.objects.all()
        serializer = CharacterPositionSerializer(character_positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(('GET',))
    def get_characters_in_location(request, location_id=None) -> Response:
        if not location_id:
            return Response("Not valid ID", status=status.HTTP_400_BAD_REQUEST)
        
        character_positions = CharacterPosition.objects.get_all_character_positions_in_location_by_id(location_id=location_id)
        serializer = CharacterPositionSerializer(character_positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(('GET',))
    def get_location(request, location_id=None) -> Response:
        if not location_id:
            return Response("Not valid ID", status=status.HTTP_400_BAD_REQUEST)
        
        location = Location.objects.get_location_by_id(location_id=location_id)
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
        
        locations = Lobby.objects.get_lobby_by_id(lobby_id=lobby_id)
        serializer = LobbySerializer(locations)
        return Response(serializer.data, status=status.HTTP_200_OK)