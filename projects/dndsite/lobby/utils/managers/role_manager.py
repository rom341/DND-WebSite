from lobby.models import LobbyMembershipUser, LobbyRole


class RoleController:
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
    def user_has_role(user, lobby, role_name):
        try:
            membership = LobbyMembershipUser.objects.get(user=user, lobby=lobby)
            return membership.role.name == role_name
        except LobbyMembershipUser.DoesNotExist:
            return False
        
    