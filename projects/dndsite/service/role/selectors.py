from lobby.models import LobbyRole


def get_role_by_name(role_name: str):
    return LobbyRole.objects.get_role_by_name(role_name=role_name)