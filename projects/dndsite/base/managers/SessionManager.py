from django.http import HttpRequest

from battlefield.models import Location
from lobby.models import Lobby


class SessionManager:
    _current_lobby_id = 'current_lobby_id'
    _current_location_id = 'current_location_id'

    def __init__(self, session: dict):
        self.session = session

    def get_current_lobby_id(self):
        return self.session.get(self._current_lobby_id)
    
    def get_current_lobby(self):
        return Lobby.objects.get_lobby_by_id(lobby_id=self.get_current_lobby_id())
    
    def get_current_location_id(self):
        return self.session.get(self._current_location_id)
    
    def get_current_location(self):
        return Location.objects.get_location_by_id(location_id=self.get_current_location_id())
    
    @staticmethod
    def get_session_manager(request: HttpRequest) -> "SessionManager":
        return SessionManager(session=request.session)
