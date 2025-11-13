from django.contrib.auth.models import User

from characters.models import Character
from groups.models import DefaultRoles, Group, GroupMembershipCharacter, GroupMembershipUser, GroupRole

class GroupManager:
    @staticmethod
    def create_group(name):
        group = Group(name=name)
        group.save()
        return group
    
    @staticmethod
    def get_group_by_id(group_id):
        try:
            return Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return None
    
    @staticmethod
    def get_characters_in_group(group):
        # Поскольку Characters связан с GroupMembership, и Group тоже связан с GroupMembership,
        # мы можем фильтровать Characters по membership__group
        # и тогда Django сделает что то вроде 
        # "SELECT * FROM Character WHERE membership IN (SELECT id FROM GroupMembership WHERE group_id = group.id)"
        return Character.objects.filter(
            positions__location__group=group
        )
    
    @staticmethod
    def get_groups_with_user(user):
        return Group.objects.filter(
            user_memberships__user=user
        )

    @staticmethod
    def get_users_in_group(group):
        return User.objects.filter(
            group_memberships__group=group
        )

    @staticmethod
    def get_characters_on_position(group, column, row):
        return Character.objects.filter(
            positions__location__group=group,
            positions__column=column,
            positions__row=row,
        )
        
    @staticmethod
    def add_character_to_group(character, group): 
        """Add character to existing group or create new membership if not exists""" 
        # Look for existing membership using Character.User and Group
        # If found, update it; if not, create a new one with the Character and role      
        membership, created = GroupMembershipCharacter.objects.get_or_create(
            group=group,
            character=character
        )
        # If the membership already existed, update the character and role
        if not created:
            membership.character = character
            membership.save()
                    
        return membership
        
    @staticmethod
    def add_user_to_group(user, group, role_name=DefaultRoles.PLAYER.value): 
        """Add user to existing group or create new membership if not exists""" 
        # Look for existing membership using User and Group
        # If found, update it; if not, create a new one with the User and role 
        role, role_created = GroupRole.objects.get_or_create(name=role_name)     
        membership, membership_created = GroupMembershipUser.objects.get_or_create(
            group=group,
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
    def is_position_occupied(group, x, y):
        return GroupManager.get_characters_on_position(group, x, y).exists()