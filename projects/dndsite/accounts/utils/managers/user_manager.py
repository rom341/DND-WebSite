from characters.models import Character


class UserManager:
    @staticmethod
    def get_user_characters(user):
        return Character.objects.filter(
            user=user
        )