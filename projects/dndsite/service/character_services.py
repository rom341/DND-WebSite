from characters.models import Character
from django.contrib.auth.models import User

def get_user_characters(user: User):
    return Character.objects.filter(
        user=user
    )