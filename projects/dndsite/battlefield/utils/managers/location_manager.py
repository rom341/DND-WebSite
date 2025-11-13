from battlefield.models import Location
from characters.models import Character


class LocationManager:
    @staticmethod
    def create_location(name, group, description="", rows_count=10, columns_count=10):
        location = Location(name=name, group=group, description=description, rows_count=rows_count, columns_count=columns_count)
        location.save()
        return location
    
    @staticmethod
    def get_location_by_id(location_id):
        try:
            return Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return None
        
    @staticmethod
    def get_locations_for_group(group):
        return Location.objects.filter(group=group)
    
    @staticmethod
    def get_characters_in_location(location):
        return Character.objects.filter(positions__location=location)
    
    @staticmethod
    def is_user_has_access_to_location(user, location):
        return location.group.user_memberships.filter(user=user).exists()
    
    @staticmethod
    def delete_location(location_id):
        location = LocationManager.get_location_by_id(location_id)
        if location:
            location.delete()
            return True
        return False
    
    
