from battlefield.models import Location
from characters.models import Character


class LocationController:
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
        if LocationController.is_user_has_access_to_location(user, location):
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
        location = LocationController.get_location_by_id(location_id)
        if location:
            location.delete()
            return True
        return False
    
    
