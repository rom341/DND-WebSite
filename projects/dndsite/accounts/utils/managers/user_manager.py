from characters.models import Character
from django.contrib.auth.models import User

class UserManager:
    @staticmethod
    def get_user_characters(user):
        return Character.objects.filter(
            user=user
        )
        
    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
    