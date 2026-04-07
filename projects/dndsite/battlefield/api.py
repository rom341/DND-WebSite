from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from location.models import CharacterPosition, Location
from battlefield.serializers import CharacterPositionSerializer, LocationSerializer
from lobby.models import Lobby
from lobby.serializers import LobbySerializer

class CharacterPositionApi(APIView):
    def get_all_character_positions(self, request) -> Response:
        character_positions = CharacterPosition.objects.all()
        serializer = CharacterPositionSerializer(character_positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(('GET',))
    def get_character_positions_in_location(request, location_id=None) -> Response:
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
    

        
    @api_view(('POST',))
    def create_location(request) -> Response:
        lobbyId = request.data.get("lobbyId")
        locationName = request.data.get("locationName")
        locationDescription = request.data.get("locationDesription")
        locationRowsCount = request.data.get("locationRowsCount")
        locationColumnsCount = request.data.get("locationColumnsCount")

        if not lobbyId or not locationName or not locationRowsCount or not locationColumnsCount:
            return Response("Not valid data", status=status.HTTP_400_BAD_REQUEST)
        
        selectedLobby = Lobby.objects.get_lobby_by_id(lobby_id=lobbyId)
        if not selectedLobby:
            return Response("Lobby with this id does not exists", status=status.HTTP_400_BAD_REQUEST)
        
        createdLocation = Location.objects.create_location(
            lobby=selectedLobby,
            name=locationName,
            description=locationDescription,
            rows_count=locationRowsCount,
            columns_count=locationColumnsCount
        )
        serializer = LocationSerializer(createdLocation)
        return Response(serializer.data, status=status.HTTP_200_OK)