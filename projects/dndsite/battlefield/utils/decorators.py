from functools import wraps

from django.http import HttpResponseForbidden

from battlefield.models import GroupMembershipUser
from battlefield.utils.model_managers.role_manager import DefaultRoles


def game_master_required(view_func):
    """
    decorator to ensure the user is a Game Master in the specified D&D group.
    Assumes that the view receives 'group_id' as a GET parameter.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        group_id = request.GET.get('group_id')
        if not group_id or not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in and specify a D&D room to access this page.")
        try:
            membership = GroupMembershipUser.objects.get(
                user=request.user, 
                group_id=group_id
            )
        except GroupMembershipUser.DoesNotExist:
            # User is not a member of this group
            return HttpResponseForbidden("You are not a member of this D&D room.")

        # 3. Role check
        # Assuming 'GM' is the Game Master role
        if membership.role.name != DefaultRoles.GAME_MASTER.value:
            return HttpResponseForbidden("Game Master privileges are required for this action.")

        # 4. If all checks pass, call the original view
        return view_func(request, *args, **kwargs)
        
    return wrapper

def group_id_in_get_required(view_func):
    """
    Decorator to ensure that 'group_id' is present in GET parameters.
    Redirects to 'groups' page if not present.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        group_id = request.GET.get('group_id')
        if not group_id:
            return HttpResponseForbidden("group_id parameter is required.")
        return view_func(request, *args, **kwargs)
    
    return wrapper

def group_membership_required(view_func):
    """
    Decorator to ensure the user is a member of the specified D&D group.
    Assumes that the view receives 'group_id' as a GET parameter.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        group_id = request.GET.get('group_id')
        if not group_id or not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in and specify a D&D room to access this page.")
        try:
            GroupMembershipUser.objects.get(
                user=request.user, 
                group_id=group_id
            )
        except GroupMembershipUser.DoesNotExist:
            # User is not a member of this group
            return HttpResponseForbidden("You are not a member of this D&D group.")

        # If check passes, call the original view
        return view_func(request, *args, **kwargs)
        
    return wrapper