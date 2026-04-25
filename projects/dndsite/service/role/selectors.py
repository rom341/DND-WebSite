from lobby.models import DefaultRoles, LobbyRole


def get_gm_role():
    return LobbyRole.objects.get_role_by_name(DefaultRoles.GAME_MASTER.value)


def get_role_by_name(role_name: str):
    return LobbyRole.objects.get_role_by_name(role_name=role_name)