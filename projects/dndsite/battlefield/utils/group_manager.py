from battlefield.models import Character, GroupMembershipCharacter, Group, GroupMembershipUser
from django.contrib.auth.models import User



class UserManager:
    @staticmethod
    def get_user_characters(user):
        return Character.objects.filter(
            user=user
        )


class GroupManager:
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
            group_memberships__group=group
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
    def get_characters_on_position(group, x, y):
        return Character.objects.filter(
            group_memberships__group=group,
            position_x=x,
            position_y=y
        )
        
    @staticmethod
    def add_character_to_group(character, group, role='player'): 
        """Add character to existing group or create new membership if not exists""" 
        # Look for existing membership using Character.User and Group
        # If found, update it; if not, create a new one with the Character and role      
        membership, created = GroupMembershipCharacter.objects.get_or_create(
            group=group,
            character=character
        )
        print(f"Adding character {character.name} to group {group.name}, created new membership: {membership}, {created}")
        # If the membership already existed, update the character and role
        if not created:
            membership.character = character
            membership.save()
                    
        return membership
        
    @staticmethod
    def add_user_to_group(user, group, role='player'): 
        """Add user to existing group or create new membership if not exists""" 
        # Look for existing membership using User and Group
        # If found, update it; if not, create a new one with the User and role      
        membership, created = GroupMembershipUser.objects.get_or_create(
            group=group,
            user=user,
            defaults={'role': role}
        )
        print(f"Adding user {user.username} to group {group.name}, created new membership: {membership}, {created}")
        # If the membership already existed, update the user and role
        if not created:
            membership.user = user
            membership.save()
            
        return membership
        
    @staticmethod
    def is_position_occupied(group, x, y):
        return GroupManager.get_characters_on_position(group, x, y).exists()