from enum import Enum
from battlefield.models import GroupMembershipUser, GroupRole

class DefaultRoles(Enum):
    GAME_MASTER = 'GM'
    PLAYER = 'Player'

class RoleManager:
    @staticmethod
    def get_role_by_name(role_name):
        try:
            return GroupRole.objects.get(name=role_name)
        except GroupRole.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_roles_in_group(user, group):
        return GroupRole.objects.filter(
            memberships__user=user,
            memberships__group=group
        )

    @staticmethod
    def user_has_role(user, group, role_name):
        try:
            membership = GroupMembershipUser.objects.get(user=user, group=group)
            return membership.role.name == role_name
        except GroupMembershipUser.DoesNotExist:
            return False
        
    