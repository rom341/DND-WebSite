from characters.models import CharacterPosition, CharacterState
from location.models import Location
from service import character_services as chars_service

def add_character_to_location(character_state: CharacterState, location: Location, target_row: int, target_column: int):
    return chars_service.create_character_position(
        character_state=character_state,
        location=location,
        row=target_row,
        column=target_column
    )
