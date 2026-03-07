from functools import wraps

from django.http import HttpResponseForbidden
from django.contrib import messages

from base.managers.SessionManager import SessionManager
from lobby.models import DefaultRoles, LobbyMembershipUser


def game_master_required(view_func):
    """
    decorator to ensure the user is a Game Master in the specified D&D lobby.
    Assumes that the view receives 'lobby_id' as a GET parameter.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        lobby_id = request.session.get('current_lobby_id')
        if not lobby_id or not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in and specify a D&D room to access this page.")
        try:
            membership = LobbyMembershipUser.objects.get(
                user=request.user, 
                lobby_id=lobby_id
            )
        except LobbyMembershipUser.DoesNotExist:
            # User is not a member of this lobby
            messages.info(request, 'You are not a member of this D&D room.')
            return HttpResponseForbidden("You are not a member of this D&D room.")

        # 3. Role check
        # Assuming 'GM' is the Game Master role
        if membership.role.name != DefaultRoles.GAME_MASTER.value:
            messages.info(request, 'Game Master privileges are required for this action.')
            return HttpResponseForbidden("Game Master privileges are required for this action.")

        # 4. If all checks pass, call the original view
        return view_func(request, *args, **kwargs)
        
    return wrapper

def lobby_id_in_session_required(view_func):
    """
    Decorator to ensure that 'lobby_id' is present in the session.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        session_manager = SessionManager.get_session_manager(request=request)
        lobby_id = session_manager.get_current_lobby_id()
        if not lobby_id:
            return HttpResponseForbidden("lobby_id parameter is required.")
        return view_func(request, *args, **kwargs)
    
    return wrapper

def lobby_membership_required(view_func):
    """
    Decorator to ensure the user is a member of the specified D&D lobby.
    Assumes that the view receives 'lobby_id' as a GET parameter.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        session_manager = SessionManager.get_session_manager(request=request)
        lobby_id = session_manager.get_current_lobby_id()
        if not lobby_id or not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in and specify a D&D room to access this page.")
        try:
            LobbyMembershipUser.objects.get(
                user=request.user, 
                lobby_id=lobby_id
            )
        except LobbyMembershipUser.DoesNotExist:
            # User is not a member of this lobby
            return HttpResponseForbidden("You are not a member of this D&D lobby.")

        # If check passes, call the original view
        return view_func(request, *args, **kwargs)
        
    return wrapper