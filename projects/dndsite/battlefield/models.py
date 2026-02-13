from django.db import models

from base.managers.UniversalManager import UniversalManager
from characters.models import Character
from lobby.models import Lobby

# Create your models here.    

class LocationManager(UniversalManager):
    @staticmethod
    def create_location(name, lobby, description="", rows_count=10, columns_count=10):
        location = Location(name=name, lobby=lobby, description=description, rows_count=rows_count, columns_count=columns_count)
        location.save()
        return location
    
    @staticmethod
    def get_location_by_id(location_id):
        try:
            return Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return None
        
    @staticmethod
    def get_locations_for_lobby(lobby):
        return Location.objects.filter(lobby=lobby)
    
    @staticmethod
    def get_characters_in_location(location):
        return Character.objects.filter(positions__location=location)
    
    @staticmethod
    def get_characters_in_location_for_user(location, user):
        if LocationManager.is_user_has_access_to_location(user, location):
            return Character.objects.filter(
                positions__location=location,
                user=user
                )
        return Character.objects.none()
    
    @staticmethod
    def is_user_has_access_to_location(user, location):
        return location.lobby.user_memberships.filter(user=user).exists()
    
    @staticmethod
    def delete_location(location_id):
        location = LocationManager.get_location_by_id(location_id)
        if location:
            location.delete()
            return True
        return False

class CharacterPositionController(UniversalManager):
    @staticmethod
    def set_character_position(character, location, row, column):
        char_pos, created = CharacterPosition.objects.get_or_create(character=character, location=location)
        char_pos.row = row
        char_pos.column = column
        char_pos.save()
        return char_pos
    
    @staticmethod
    def get_character_position_in_location(character, location):
        try:
            return CharacterPosition.objects.get(character=character, location=location)
        except CharacterPosition.DoesNotExist:
            return None
        
    @staticmethod
    def get_all_character_positions_in_location(location):
        return CharacterPosition.objects.filter(location=location)
        
    @staticmethod
    def get_characters_in_location(location):
        return CharacterPosition.objects.filter(location=location)
    
    @staticmethod
    def move_character(character, location, new_row, new_column):
        character_position = CharacterPositionController.get_character_position_in_location(character, location)
        if character_position:
            character_position.row = new_row
            character_position.column = new_column
            character_position.save()
            return character_position
        return None
    
    @staticmethod
    def is_position_occupied(location, column, row):
        return CharacterPosition.objects.filter(location=location, column=column, row=row).exists()

class Location(models.Model):
    objects: LocationManager = LocationManager()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    rows_count = models.IntegerField(default=10)
    columns_count = models.IntegerField(default=10)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"{self.name} ({self.rows_count}x{self.columns_count})"
    
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