from characters.models import Character, EntityBase, CharacterState, CharacterPosition, HealActionType
from lobby.models import Lobby, DefaultRoles, LobbyRole
from location.models import Location

def create_entity_base(entity_base_name: str, character_class: str = None, race: str = None, 
    alignment: str = None, size: str = None, age: int = None, height: str = None, 
    weight: str = None, mastery: int = 0) -> EntityBase:
    return EntityBase.objects.create(
        entity_base_name=entity_base_name, character_class=character_class, race=race,
        alignment=alignment, size=size, age=age, height=height, weight=weight, mastery=mastery
    )

def get_entity_base_by_id(id: int) -> EntityBase:
    return EntityBase.objects.get(id=id)

def get_all_entity_bases() -> list[EntityBase]:
    return EntityBase.objects.all()

def create_npc(user, entity_base: EntityBase, count: int = 1):
    created = []
    for i in range(count):
        created.append(Character.objects.create_character_for_npc(user, entity_base))
    return created

def get_character_by_id(character_id: int) -> Character:
    return Character.objects.get(id=character_id)

def create_character(user, character_name: str, entity_base_id: int, level: int = 1, 
    experience: int = 0, max_hit_points: int = 0, is_npc: bool = False,
    money=None, stats=None, spell_circle_slots=None):
    return Character.objects.create(
        user=user, character_name=character_name, entity_base_id=entity_base_id,
        level=level, experience=experience, max_hit_points=max_hit_points,
        is_npc=is_npc, money=money, stats=stats, spell_circle_slots=spell_circle_slots
    )

def create_character_for_npc(user, entity_base: EntityBase):
    return Character.objects.create(
        user=user, character_name=f"npc_{entity_base.entity_base_name}",
        entity_base_id=entity_base.id, max_hit_points=entity_base.max_hit_points, is_npc=True
    )

def get_characters_available_for_user_in_location(user, location: Location):
    if LobbyRole.objects.user_has_role(user=user, lobby=location.lobby, role=DefaultRoles.GAME_MASTER):
        return Location.objects.get_characters_in_location(location=location)
    else:
        return Location.objects.get_characters_in_location_for_user(user=user, location=location)

def change_health(character: Character, heal_value: int, heal_type: int):
    if not character:
        raise ValueError("Character cannot be None")
    
    health_change_value = heal_value * -1 if heal_type == HealActionType.Heal else 1
    new_health = max(-10000, min(character.current_hit_points + health_change_value, character.entity_base.max_hit_points))
    character.current_hit_points = new_health
    character.save()

def create_character_state(character: Character, lobby: Lobby) -> CharacterState:
    return CharacterState.objects.create(
        character=character, lobby=lobby, current_hit_points=character.max_hit_points
    )

def get_or_create_character_state_for_lobby(character: Character, lobby: Lobby):
    try:
        return CharacterState.objects.get(character=character, lobby=lobby)
    except CharacterState.DoesNotExist:
        print(f"Creating new character state for '{character.character_name}' in lobby '{lobby.name}'")
        return create_character_state(character, lobby)

def create_character_position(character_state: CharacterState, location: Location, row: int, column: int):
    return CharacterPosition.objects.create(
        character_state=character_state, location=location, row=row, column=column
    )

def set_character_position(character_state: CharacterState, location: Location, row: int, column: int):
    character_position = CharacterPosition.objects.get(character_state=character_state, location=location)
    character_position.row = row
    character_position.column = column
    character_position.save()
    return character_position

def get_character_position_in_location(character: Character, location: Location):
    try:
        return CharacterPosition.objects.get(
            character_state__character=character, location=location
        )
    except CharacterPosition.DoesNotExist:
        print(f"Character '{character.character_name}' has no position in location '{location.name}'")
        return None

def get_all_character_positions_in_location(location: Location):
    return CharacterPosition.objects.filter(location=location)

def get_all_character_positions_in_location_by_id(location_id: int):
    return CharacterPosition.objects.filter(location__id=location_id)

def move_character(character: Character, location: Location, new_row: int, new_column: int):
    current_position = get_character_position_in_location(character, location)
    
    if not current_position:
        print(f"Character '{character.character_name}' has no position in location '{location.name}', cannot move")
        return None
    
    if CharacterPosition.objects.filter(location=location, row=new_row, column=new_column).exists():
        print(f"Cannot move character '{character.character_name}' to ({new_row}, {new_column}) - position occupied")
        return None
    
    character_position = CharacterPosition.objects.get(
        character_state__character=character, location=location
    )
    character_position.row = new_row
    character_position.column = new_column
    character_position.save()
    return character_position

def is_position_occupied(location: Location, row: int, column: int):
    return CharacterPosition.objects.filter(location=location, row=row, column=column).exists()
