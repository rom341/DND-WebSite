from django.shortcuts import redirect, render

from groups.models import DefaultRoles, Group
from groups.utils.managers.group_manager import GroupManager
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
@login_required
def groups(request):
    user = request.user    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        try:
            with transaction.atomic(): # Ensure that the whole function is atomic (all-or-nothing)
                if action == 'select': # group selected
                    group_id = request.POST.get('group_id')
                    group = GroupManager.get_group_by_id(group_id)
                    characters = GroupManager.get_characters_in_group(group)
                    return redirect(f'/battle/?group_id={group_id}')
                
                elif action == 'create': # new group created
                    new_group_name = request.POST.get('group_name')
                    new_group = Group(name=new_group_name)
                    new_group.save()
                    GroupManager.add_user_to_group(user, new_group, role_name=DefaultRoles.GAME_MASTER.value)
                    return redirect(f'/battle/?group_id={new_group.id}')
        except Exception as e:
            pass
    groups = GroupManager.get_groups_with_user(user)   
    data = {
        'groups': groups,
    }

    return render(request, 'groups.html', data)