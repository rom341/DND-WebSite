from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from battlefield.forms.add_character_to_group_form import AddCharacterToGroupForm
from battlefield.forms.add_user_to_group_form import AddUserToGroupForm
from battlefield.forms.create_location_form import CreateLocationForm
from battlefield.forms.move_character_form import MoveCharacterForm
from battlefield.utils.contexts.battle_context import BattlefieldContextContainer
from battlefield.utils.contexts.character_position_context import CharacterPositionContextContainer
from battlefield.utils.contexts.location_map_context import LocationMapContextContainer
from battlefield.utils.contexts.locations_list_context import LocationsListContextContainer
from battlefield.utils.decorators import game_master_required, group_id_in_session_required, group_membership_required
from battlefield.utils.managers.character_position_manager import CharacterPositionManager
from battlefield.utils.managers.location_manager import LocationManager
from characters.utils.managers.character_manager import CharacterManager
from groups.utils.managers.group_manager import GroupManager


# Create your views here.
@login_required
@game_master_required
def add_character_to_group(request):
    if request.method == 'POST':
        group_id = request.session.get('current_group_id')
        group = GroupManager.get_group_by_id(group_id)
        character_id = request.POST.get('character_id')
        character = CharacterManager.get_character_by_id(character_id)
        form = AddCharacterToGroupForm(request.POST, group=group)
        if form.is_valid():
            if group:
                current_location_id = request.POST.get('location_id')
                location = LocationManager.get_location_by_id(current_location_id)
                target_row = form.cleaned_data['target_row']
                target_column = form.cleaned_data['target_column']
                CharacterPositionManager.set_character_position(
                    character=character,
                    location=location,
                    row=target_row,
                    column=target_column
                )
                context_container = BattlefieldContextContainer(
                    current_group_id=group_id,
                    current_group=group,
                    characters_list=GroupManager.get_characters_in_group(group),
                    add_character_form=form
                )
                context = context_container.get_context()
                return render(request, 'partials/battle_map.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")

@login_required
@game_master_required
def add_user_to_group(request):
    if request.method == 'POST':
        group_id = request.session.get('current_group_id')
        group = GroupManager.get_group_by_id(group_id)
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        current_location_id = request.session.get('current_location_id')
        location = LocationManager.get_location_by_id(current_location_id)
        form = AddUserToGroupForm(request.POST, group=group)
        if form.is_valid():
            if group:
                GroupManager.add_user_to_group(user, group)
                context = {
                    'users_list': GroupManager.get_users_in_group(group),
                }
                return render(request, 'partials/users_list.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")

@login_required
@game_master_required
def create_location(request):
    if request.method == 'POST':
        group_id = request.session.get('current_group_id')
        group = GroupManager.get_group_by_id(group_id)
        form = CreateLocationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            rows_count = form.cleaned_data['rows_count']
            columns_count = form.cleaned_data['columns_count']
            created_location = LocationManager.create_location(
                name=name,
                group=group,
                description=description,
                rows_count=rows_count,
                columns_count=columns_count
            )
            context_container = LocationsListContextContainer(
                locations_list=LocationManager.get_locations_for_group(group)
            )
            context = context_container.get_context()
            return render(request, 'partials/locations_list.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
def select_location(request):
    if request.method == 'POST':
        location_id = request.POST.get('location_id')
        location = LocationManager.get_location_by_id(location_id)
        if location and LocationManager.is_user_has_access_to_location(request.user, location):
            request.session['current_location_id'] = location.id
            
            character_positions_context_container = CharacterPositionContextContainer(
                character_positions=CharacterPositionManager.get_all_character_positions_in_location(location)
            )
            
            location_map_context_container = LocationMapContextContainer(
                current_location_id=location.id,
                current_location=location,
                rows_count=location.rows_count,
                cols_count=location.columns_count,
                characters_list=LocationManager.get_characters_in_location(location),
                character_position_context=character_positions_context_container
            )
            context = location_map_context_container.get_context()
            return render(request, 'partials/battle_map.html', context)
    return HttpResponseBadRequest("Location not found.")

@login_required
@group_id_in_session_required
@group_membership_required
def battlefield(request):    
    current_group_id = request.session.get('current_group_id')
    group = GroupManager.get_group_by_id(current_group_id)  
    current_location_id = request.session.get('current_location_id')
    print(f"Selected location ID in session: {current_location_id}")
    
    characters_in_current_location = []
    locations_list = []
    selected_location = None
    rows_count = 0
    cols_count = 0
    move_character_form = None
    add_character_form = None
    add_user_form = AddUserToGroupForm(group=group)
    create_location_form = CreateLocationForm()
    
    if current_location_id:
        selected_location = LocationManager.get_location_by_id(current_location_id)
        
        rows_count = selected_location.rows_count
        cols_count = selected_location.columns_count
        
        characters_in_current_location = LocationManager.get_characters_in_location(selected_location)
        locations_list = LocationManager.get_locations_for_group(group)
        
        move_character_form = MoveCharacterForm(group=group, location=selected_location)    
        add_character_form = AddCharacterToGroupForm(group=group)        
    else:
        locations_list = LocationManager.get_locations_for_group(group)
    
    character_positions_context_container = CharacterPositionContextContainer(
        character_positions=CharacterPositionManager.get_all_character_positions_in_location(selected_location)
    )
    
    location_context_container = LocationMapContextContainer(
        current_location_id=current_location_id,
        current_location=selected_location,
        rows_count=rows_count,
        cols_count=cols_count,
        characters_list=characters_in_current_location,
        character_position_context=character_positions_context_container
    )
    
    battlefield_context_container = BattlefieldContextContainer(
        current_group_id=current_group_id,
        current_group=group,
        locations_list=locations_list,
        users_list=GroupManager.get_users_in_group(group),
        move_character_form=move_character_form,
        add_character_form=add_character_form,
        add_user_form=add_user_form,
        create_location_form=create_location_form,
        location_map_context=location_context_container
    )
    context = battlefield_context_container.get_context()
    return render(request, 'battlefield.html', context)
    