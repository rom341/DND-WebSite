from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from battlefield.forms.add_character_to_group_form import AddCharacterToGroupForm
from battlefield.forms.add_user_to_group_form import AddUserToGroupForm
from battlefield.forms.move_character_form import MoveCharacterForm
from battlefield.utils.contexts.battle_context import BattlefieldContextContainer
from battlefield.utils.decorators import game_master_required, group_id_in_get_required, group_membership_required
from characters.models import Character
from groups.utils.managers.group_manager import GroupManager


# Create your views here.
@game_master_required
def add_character_to_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = GroupManager.get_group_by_id(group_id)
        character_id = request.POST.get('character_id')
        character = Character.objects.get(id=character_id)
        form = AddCharacterToGroupForm(request.POST, group=group)
        if form.is_valid():
            if group:
                GroupManager.add_character_to_group(character, group)
                context = {
                    'rows_count': 10,
                    'cols_count': 5,
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group),
                    'add_character_form': form
                }
                return render(request, 'partials/battle_map.html', context)
    else:
        form = AddCharacterToGroupForm()

    return render(request, 'partials/battle_map.html', {
                    'rows_count': 10,
                    'cols_count': 5,
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group) if group else [],
                    'add_character_form': form
                })

@game_master_required
def add_user_to_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = GroupManager.get_group_by_id(group_id)
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        form = AddUserToGroupForm(request.POST, group=group)
        if form.is_valid():
            if group:
                GroupManager.add_user_to_group(user, group)
                context = {
                    'rows_count': 10,
                    'cols_count': 5,
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group),
                    'add_user_form': form
                }
                return render(request, 'partials/battle_map.html', context)
    else:
        form = AddUserToGroupForm()

    return render(request, 'partials/battle_map.html', {
                    'rows_count': 10,
                    'cols_count': 5,
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group) if group else [],
                    'add_user_form': form
                })

@login_required
@group_id_in_get_required
@group_membership_required
def battle(request):    
    group_id = request.GET.get('group_id')
    group = GroupManager.get_group_by_id(group_id)
    
    characters = GroupManager.get_characters_in_group(group) 
    move_character_form = MoveCharacterForm(group=group)    
    add_character_form = AddCharacterToGroupForm(group=group)
    add_user_form = AddUserToGroupForm(group=group)
    contextContainer = BattlefieldContextContainer(
        group_id=group_id,
        rows_count=10,
        cols_count=5,
        characters=characters,
        move_character_form=move_character_form,
        add_character_form=add_character_form,
        add_user_form=add_user_form
    )
    context = contextContainer.get_context()
    return render(request, 'battlefield.html', context)
    