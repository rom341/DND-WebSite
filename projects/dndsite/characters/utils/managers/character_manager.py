from characters.models import Character


class CharacterManager:
    @staticmethod
    def get_character_by_id(character_id):
        return Character.objects.get(id=character_id)