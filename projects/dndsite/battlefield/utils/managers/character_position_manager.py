from battlefield.models import CharacterPosition


class CharacterPositionManager:
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
        character_position = CharacterPositionManager.get_character_position_in_location(character, location)
        if character_position:
            character_position.row = new_row
            character_position.column = new_column
            character_position.save()
            return character_position
        return None
    
    @staticmethod
    def is_position_occupied(location, column, row):
        return CharacterPosition.objects.filter(location=location, column=column, row=row).exists()