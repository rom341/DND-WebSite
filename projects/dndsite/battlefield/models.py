from typing import Optional
from django.db import models
from django.contrib.auth.models import User

from base.managers.UniversalManager import UniversalManager
from battlefield.utils.contexts.character_position_context import CharacterPositionContextContainer
from battlefield.utils.contexts.location_map_context import LocationMapContextContainer
from characters.models import Character, CharacterController
from lobby.models import Lobby


# Create your models here.    

class LocationManager(UniversalManager):
    def create_location(self, name, lobby, description="", rows_count=10, columns_count=10) -> 'Location':
        location = Location(name=name, lobby=lobby, description=description, rows_count=rows_count, columns_count=columns_count)
        location.save()
        return location
    
    def get_location_by_id(self, location_id) -> 'Location':
        try:
            return Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return None
        
    def get_locations_for_lobby(self, lobby: Lobby) -> 'LocationManager':
        return Location.objects.filter(lobby=lobby)
    
    def get_characters_in_location(self, location: 'Location') -> CharacterController:
        return Character.objects.filter(positions__location=location)
    
    def get_characters_in_location_for_user(self, user: User, location: 'Location') -> CharacterController:
        if LocationManager.is_user_has_access_to_location(user, user, location):
            return Character.objects.filter(
                positions__location=location,
                user=user
                )
        return Character.objects.none()
    
    def is_user_has_access_to_location(self, user: 'User', location: 'Location') -> bool:
        return location.lobby.user_memberships.filter(user=user).exists()
    
    def delete_location(self, location_id: int):
        location = LocationManager.get_location_by_id(location_id)
        if location:
            location.delete()
            return True
        return False

class Location(models.Model):
    objects: LocationManager = LocationManager()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    rows_count = models.IntegerField(default=10)
    columns_count = models.IntegerField(default=10)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"{self.name} ({self.rows_count}x{self.columns_count})"
    
    
    def to_context(self, character_position_context_container: CharacterPositionContextContainer = None) -> LocationMapContextContainer:
        return LocationMapContextContainer(
                    current_location_id=self.id,
                    rows_count=self.rows_count,
                    cols_count=self.columns_count,
                    characters_list=Location.objects.get_characters_in_location(location=self),
                    character_position_context=character_position_context_container
                )

class CharacterPositionController(UniversalManager):
    def set_character_position(self, character: Character, location: Location, row: int, column: int) -> 'CharacterPosition':
        character_position, created = CharacterPosition.objects.get_or_create(character=character, location=location)
        character_position.row = row
        character_position.column = column
        character_position.save()
        return character_position
    
    def get_character_position_in_location(self, character: Character, location: Location) -> Optional["CharacterPositionController"]:
        try:
            return CharacterPosition.objects.get(character=character, location=location)
        except CharacterPosition.DoesNotExist:
            return None
        
    def get_all_character_positions_in_location(self, location: Location) -> "CharacterPositionController":
        return CharacterPosition.objects.filter(location=location)
        
    def get_characters_in_location(self, location: Location) -> "CharacterPositionController":
        return CharacterPosition.objects.filter(location=location)
    
    def move_character(self, character: Character, location: Location, new_row: int, new_column: int) -> Optional["CharacterPosition"]:
        character_position = CharacterPositionController.get_character_position_in_location(character, location)
        if character_position:
            character_position.row = new_row
            character_position.column = new_column
            character_position.save()
            return character_position
        return None
    
    def is_position_occupied(self, location: Location, column: int, row: int) -> bool:
        return CharacterPosition.objects.filter(location=location, column=column, row=row).exists()
    
class CharacterPosition(models.Model):
    objects: CharacterPositionController = CharacterPositionController()
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='positions')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='character_positions')
    row = models.IntegerField(default=0)
    column = models.IntegerField(default=0)

    class Meta:
        unique_together = ('character', 'location')

    def __str__(self):
        return f"{self.character.character_name} at ({self.row}, {self.column}) in {self.location.name}"
    
    def to_context(self, location: Location) -> CharacterPositionContextContainer:
        return CharacterPositionContextContainer(
                    character_positions=CharacterPosition.objects.get_all_character_positions_in_location(location=location)
                )