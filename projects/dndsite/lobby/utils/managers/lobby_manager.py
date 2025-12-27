from django.contrib.auth.models import User

from characters.models import Character
from lobby.models import DefaultRoles, Lobby, LobbyMembershipCharacter, LobbyMembershipUser, LobbyRole

class GroupManager:
    @staticmethod
    def create_lobby(name) -> Lobby:
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
    def get_lobby_with_user(user):
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
        role, role_created = LobbyRole.objects.get_or_create(name=role_name)     
        membership, membership_created = LobbyMembershipUser.objects.get_or_create(
            lobby=lobby,
            user=user,
            defaults={'role': role}
        )
        # If the membership already existed, update the user and role
        if not role_created:
            membership.role = role
            membership.save()
        if not membership_created:
            membership.user = user
            membership.save()
            
        return membership
        
    @staticmethod
    def is_position_occupied(lobby, x, y):
        return GroupManager.get_characters_on_position(lobby, x, y).exists()