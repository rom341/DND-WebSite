from characters.models import Character, EntityBase


class CharacterManager:
    @staticmethod
    def get_character_by_id(character_id):
        return Character.objects.get(id=character_id)
    
    @staticmethod
    def get_all_character_model_templates():
        return EntityBase.objects.all()