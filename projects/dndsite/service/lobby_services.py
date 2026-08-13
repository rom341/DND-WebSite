from characters.models import Character, CharacterPosition, CharacterState
from lobby.models import DefaultRoles, Lobby, LobbyMembershipUser, LobbyRole
from django.contrib.auth.models import User
from django.db import transaction
from location.models import Location
from service import role_services as RoleSelectors
from service import character_services as chars_service

def create_lobby_with_gm(gm_user: User, new_lobby_name: str):
    with transaction.atomic:
        new_lobby = create_lobby(new_lobby_name=new_lobby_name)
        add_user_as_gm_to_lobby(user=gm_user, lobby=new_lobby)
        return new_lobby

def add_user_as_player_to_lobby(user: User, lobby: Lobby):
    add_user_to_lobby(user=user, lobby=lobby)        
    gm_role = RoleSelectors.get_role_by_name(DefaultRoles.PLAYER.value)
    set_user_role_in_lobby(user=user, lobby=lobby, role=gm_role)

def add_user_as_gm_to_lobby(user: User, lobby: Lobby):
    add_user_to_lobby(user=user, lobby=lobby)        
    gm_role = RoleSelectors.get_role_by_name(DefaultRoles.GAME_MASTER.value)
    set_user_role_in_lobby(user=user, lobby=lobby, role=gm_role)
    
def add_character_to_lobby(character: Character, lobby: Lobby):
    new_character_state = chars_service.create_character_state(character, lobby)
    return new_character_state

def create_lobby(new_lobby_name: str):
    return Lobby.objects.create_lobby(new_lobby_name)

def add_user_to_lobby(user: User, lobby: Lobby):
    Lobby.objects.add_user_to_lobby(user=user, lobby=lobby)

def set_user_role_in_lobby(user: User, lobby: Lobby, role: LobbyRole):
    LobbyMembershipUser.objects.set_user_role_in_lobby(user=user, lobby=lobby, role=role)