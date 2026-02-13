from django.db import models

from characters.models import Character
from django.contrib.auth.models import User

# Create your models here.
class UserManager:
    @staticmethod
    def get_user_characters(user: User):
        return Character.objects.filter(
            user=user
        )
        
    @staticmethod
    def get_user_by_id(user_id: int):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None