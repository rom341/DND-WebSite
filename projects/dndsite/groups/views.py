from django.shortcuts import redirect, render

from groups.models import DefaultRoles
from groups.utils.managers.group_manager import GroupManager
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
@login_required
def groups(request):
    active_user = request.user    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        try:
            with transaction.atomic(): # Ensure that the whole function is atomic (all-or-nothing)
                if action == 'select': # group selected
                    group_id = request.session.get('current_group_id')                
                elif action == 'create': # new group created
                    new_group_name = request.POST.get('group_name')
                    new_group = GroupManager.create_group(new_group_name)
                    GroupManager.add_user_to_group(active_user, new_group, role_name=DefaultRoles.GAME_MASTER.value)
                    group_id = new_group.id
                    
                request.session['current_group_id'] = group_id
                return redirect('/battlefield/')
        except Exception as e:
            pass
        
    groups = GroupManager.get_groups_with_user(active_user)   
    data = {
        'groups': groups,
    }

    return render(request, 'groups.html', data)