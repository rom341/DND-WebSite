from typing import Optional
from django.db import models
from django.contrib.auth.models import User
from core.managers.UniversalManager import UniversalManager
from lobby.models import Lobby


# Create your models here.    

class LocationManager(UniversalManager):
    def create_location(self, name, lobby, description="", rows_count=10, columns_count=10) -> 'Location':
        location = Location(name=name, lobby=lobby, description=description, rows_count=rows_count, columns_count=columns_count)
        location.save()
        return location
    
    def get_location_by_id(self, location_id: int) -> 'Location':
        try:
            return Location.objects.get(id=location_id)
        except:
            return None
        
    def get_locations_for_lobby_by_id(self, lobby_id: int) -> 'LocationManager':
        return Location.objects.filter(lobby__id=lobby_id)

    def get_locations_for_lobby(self, lobby: Lobby) -> 'LocationManager':
        return Location.objects.filter(lobby=lobby)
    
    def get_characters_in_location(self, location: 'Location'):
        from characters.models import Character

        return Character.objects.filter(states__position__location=location)
    
    def get_characters_in_location_for_user(self, user: User, location: 'Location'):
        from characters.models import Character

        if LocationManager.is_user_has_access_to_location(user, user, location):
            return Character.objects.filter(
                states__position__location=location,
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

