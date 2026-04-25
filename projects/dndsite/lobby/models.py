from enum import Enum
from django.db import models
from django.contrib.auth.models import User

from core.managers.UniversalManager import UniversalManager
from characters.models import Character

# Create your models here.
class DefaultRoles(Enum):
    GAME_MASTER = 'GM'
    PLAYER = 'Player'

class LobbyManager(UniversalManager):
    @staticmethod
    def create_lobby(name) -> "Lobby":
        lobby = Lobby(name=name)
        lobby.save()
        return lobby
    
    @staticmethod
    def get_lobby_by_id(lobby_id):
        try:
            return Lobby.objects.get(id=lobby_id)
        except Lobby.DoesNotExist:
            return None
    
    @staticmethod
    def get_characters_in_lobby(lobby):
        # Поскольку Characters связан с GroupMembership, и Group тоже связан с GroupMembership,
        # мы можем фильтровать Characters по membership__lobby
        # и тогда Django сделает что то вроде 
        # "SELECT * FROM Character WHERE membership IN (SELECT id FROM GroupMembership WHERE lobby_id = lobby.id)"
        return Character.objects.filter(
            positions__location__lobby=lobby
        )
    
    @staticmethod
    def get_lobbys_with_user(user):
        return Lobby.objects.filter(
            user_memberships__user=user
        )

    @staticmethod
    def get_users_in_lobby(lobby):
        return User.objects.filter(
            lobby_memberships__lobby=lobby
        )

    @staticmethod
    def get_characters_on_position(lobby, column, row):
        return Character.objects.filter(
            positions__location__lobby=lobby,
            positions__column=column,
            positions__row=row,
        )
        
    @staticmethod
    def add_character_to_lobby(character, lobby): 
        """Add character to existing lobby or create new membership if not exists""" 
        # Look for existing membership using Character.User and Group
        # If found, update it; if not, create a new one with the Character and role      
        membership, created = LobbyMembershipCharacter.objects.get_or_create(
            lobby=lobby,
            character=character
        )
        # If the membership already existed, update the character and role
        if not created:
            membership.character = character
            membership.save()
                    
        return membership
        
    @staticmethod
    def add_user_to_lobby(user, lobby, role_name=DefaultRoles.PLAYER.value): 
        """Add user to existing lobby or create new membership if not exists""" 
        # Look for existing membership using User and Group
        # If found, update it; if not, create a new one with the User and role 
        role = LobbyRole.objects.first()     
        membership = LobbyMembershipUser.objects.create(
            lobby=lobby,
            user=user,
            defaults={'role': role}
        )
            
        membership.save()
        return membership
        
    @staticmethod
    def is_position_occupied(lobby, x, y):
        return LobbyManager.get_characters_on_position(lobby, x, y).exists()

class Lobby(models.Model):
    objects: LobbyManager = LobbyManager()
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RoleManager(UniversalManager):
    @staticmethod
    def get_role_by_name(role_name):
        try:
            return LobbyRole.objects.get(name=role_name)
        except LobbyRole.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_roles_in_lobby(user, lobby):
        return LobbyRole.objects.filter(
            memberships__user=user,
            memberships__lobby=lobby
        )

    @staticmethod
    def user_has_role(user, lobby, role):
        try:
            membership = LobbyMembershipUser.objects.get(user=user, lobby=lobby)
            return membership.role.name == role.value
        except LobbyMembershipUser.DoesNotExist:
            return False

class LobbyRole(models.Model):
    objects: RoleManager = RoleManager()
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class LobbyMembershipUserManager(UniversalManager):
    @staticmethod
    def set_user_role_in_lobby(user: User, lobby: Lobby, role: LobbyRole):
        membership = LobbyMembershipUser.objects.get(user=user, lobby=lobby)
        membership.role = role
        membership.save()

class LobbyMembershipUser(models.Model): 
    objects: LobbyMembershipUserManager = LobbyMembershipUserManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lobby_memberships')
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='user_memberships')
    role = models.ForeignKey(LobbyRole, on_delete=models.CASCADE, related_name='memberships')

    class Meta:
        unique_together = ('user', 'lobby')
        
    def __str__(self):
        return f"{self.user.username} ({self.role}) in {self.lobby.name}"

class LobbyMembershipCharacter(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='lobby_memberships')
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='character_memberships')

    class Meta:
        unique_together = ('character', 'lobby')

    def __str__(self):
        return f"{self.character.character_name} in {self.lobby.name}"