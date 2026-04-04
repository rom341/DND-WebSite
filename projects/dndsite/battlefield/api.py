from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from battlefield.models import CharacterPosition, Location
from battlefield.serializers import CharacterPositionSerializer, LocationSerializer

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