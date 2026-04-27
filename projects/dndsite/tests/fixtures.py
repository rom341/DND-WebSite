import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from characters.models import Character, EntityBase
from lobby.models import DefaultRoles, Lobby, LobbyMembershipUser, LobbyRole
from location.models import Location
from service.role_services import get_gm_role

from django.conf import settings

@pytest.fixture(autouse=True)
def use_fast_password_hasher(settings):
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user_credentials_admin():
    return dict(
        username="admin", email="admin@gmail.com", password="admin", first_name="admin", last_name="admin"
    )

@pytest.fixture
def user_credentials_player():
    return dict(
        username="user1", email="user1@gmail.com", password="user1", first_name="user1", last_name="user1"
    )

@pytest.fixture
def default_test_users_list(db):
    users = []
    admin = User.objects.create_superuser(username="admin", email="admin@gmail.com", password="admin")
    users.append(admin)
    
    for i in range(2):
        user = User.objects.create_user(username=f"user{i}", email=f"user{i}@gmail.com", password=f"user{i}")
        users.append(user)
    
    return users

@pytest.fixture
def default_test_characters_list(db, default_test_users_list):
    characters = []
    for user in default_test_users_list:
        for i in range(2):
            entity_base = EntityBase.objects.create_entity_base(
                entity_base_name=f"{user.username}_entity_base_{i}"
            )
            
            character = Character.objects.create_character(
                user=user,
                character_name=f"{user.username}_character_{i}",
                entity_base_id=entity_base.id,
            )
            
            characters.append(character)
    return characters

@pytest.fixture
def default_test_roles_list(db):
    roles = [
    LobbyRole.objects.create_role(DefaultRoles.GAME_MASTER.value),
    LobbyRole.objects.create_role(DefaultRoles.PLAYER.value)
    ]
    
    return roles

@pytest.fixture
def default_test_lobbys_list(db, default_test_roles_list, default_test_users_list):
    lobbys = []
    for user in default_test_users_list:
        for i in range(2):
            lobby = Lobby.objects.create_lobby(f"{user.username}_lobby_{i}")
            userMembership = Lobby.objects.add_user_to_lobby(user, lobby)
            a = LobbyMembershipUser.objects.set_role(userMembership, get_gm_role())
            lobbys.append(lobby)
            
    return lobbys

@pytest.fixture
def default_test_locations_list(db, default_test_lobbys_list):
    locations = []
    for lobby in default_test_lobbys_list:
        for i in range(2):
            location = Location.objects.create_location(
                name=f"{lobby.name}_location_{i}",
                lobby=lobby,
            )
            locations.append(location)
            
    return locations
    
    
@pytest.fixture
def user_admin(default_test_users_list):
    return default_test_users_list[0]

@pytest.fixture
def user_player(default_test_users_list):
    return default_test_users_list[1]

@pytest.fixture
def auth_client_admin(user_admin, client):
    client.force_authenticate(user=user_admin)
    return client
    
@pytest.fixture
def auth_client_player(user_player, client):
    client.force_authenticate(user=user_player)
    return client