from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from battlefield.forms.add_character_to_lobby_form import AddCharacterToGroupForm
from battlefield.forms.add_npc_to_lobby_form import AddNPCToLobbyForm
from battlefield.forms.add_user_to_lobby_form import AddUserToGroupForm
from battlefield.forms.create_location_form import CreateLocationForm
from battlefield.forms.move_character_form import MoveCharacterForm
from battlefield.models import CharacterPosition, Location
from battlefield.utils.contexts.battle_context import BattlefieldContextContainer
from battlefield.utils.contexts.character_position_context import CharacterPositionContextContainer
from battlefield.utils.contexts.location_map_context import LocationMapContextContainer
from battlefield.utils.contexts.locations_list_context import LocationsListContextContainer
from battlefield.utils.decorators import game_master_required, lobby_id_in_session_required, lobby_membership_required
from characters.models import Character, EntityBase
from lobby.models import DefaultRoles, Lobby, LobbyRole


# Create your views here.
@login_required
@game_master_required
def add_user_to_lobby(request):
    if request.method == 'POST':
        lobby_id = request.session.get('current_lobby_id')
        lobby = Lobby.objects.get_lobby_by_id(lobby_id)
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        form = AddUserToGroupForm(request.POST, lobby=lobby)
        if form.is_valid():
            if lobby:
                Lobby.objects.add_user_to_lobby(user, lobby)
                context = {
                    'users_list': Lobby.objects.get_users_in_lobby(lobby),
                }
                return render(request, 'partials/users_list.html', context)
    
    return HttpResponseBadRequest("Invalid request method.")

@login_required
@game_master_required
def add_character_to_lobby(request):
    if request.method == 'POST':
        lobby_id = request.session.get('current_lobby_id')
        lobby = Lobby.objects.get_lobby_by_id(lobby_id)
        character_id = request.POST.get('character_id')
        character = Character.objects.get_character_by_id(character_id)
        form = AddCharacterToGroupForm(request.POST, lobby=lobby)
        if form.is_valid():
            if lobby:
                current_location_id = request.POST.get('location_id')
                location = Location.objects.get_location_by_id(current_location_id)
                target_row = form.cleaned_data['target_row']
                target_column = form.cleaned_data['target_column']
                CharacterPosition.objects.set_character_position(
                    character=character,
                    location=location,
                    row=target_row,
                    column=target_column
                )

                character_positions_context_container = CharacterPositionContextContainer(
                    character_positions=CharacterPosition.objects.get_all_character_positions_in_location(location)
                )
                location_context_container = LocationMapContextContainer(
                    current_location_id=current_location_id,
                    rows_count=location.rows_count,
                    cols_count=location.columns_count,
                    characters_list=Location.objects.get_characters_in_location(location),
                    character_position_context=character_positions_context_container
                )
                context_container = BattlefieldContextContainer(
                    current_lobby_id=lobby_id,
                    current_lobby=lobby,
                    location_map_context=location_context_container,
                    add_character_form=form
                )
                context = context_container.get_context()
                return render(request, 'partials/battle_map.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")

@login_required
@game_master_required
def add_npc_to_lobby(request):
    if request.method == 'POST':
        lobby_id = request.session.get('current_lobby_id')
        lobby = Lobby.objects.get_lobby_by_id(lobby_id)
        form = AddNPCToLobbyForm(request.POST, lobby=lobby)
        if form.is_valid():
            if lobby:
                entity_base = form.cleaned_data.get('entity_base')
                count = form.cleaned_data.get('count', 0)
                location = form.cleaned_data.get("location")
                created_characters_npc_list = EntityBase.objects.create_npc(request.user, entity_base, count)
                
                target_row = 0
                target_column = 0
                for character in created_characters_npc_list:
                    CharacterPosition.objects.set_character_position(
                        character=character,
                        location=location,
                        row=target_row,
                        column=target_column
                    )

                character_positions_context_container = CharacterPositionContextContainer(
                    character_positions=CharacterPosition.objects.get_all_character_positions_in_location(location=location)
                )
                location_context_container = LocationMapContextContainer(
                    current_location_id=location.id,
                    rows_count=location.rows_count,
                    cols_count=location.columns_count,
                    characters_list=Location.objects.get_characters_in_location(location=location),
                    character_position_context=character_positions_context_container
                )
                context_container = BattlefieldContextContainer(
                    current_lobby_id=lobby_id,
                    current_lobby=lobby,
                    location_map_context=location_context_container,
                    add_character_form=form
                )
                context = context_container.get_context()
                return render(request, 'partials/battle_map.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")

@login_required
@game_master_required
def create_location(request):
    if request.method == 'POST':
        lobby_id = request.session.get('current_lobby_id')
        lobby = Lobby.objects.get_lobby_by_id(lobby_id)
        form = CreateLocationForm(request.POST)
        if form.is_valid():
            form.instance.lobby = lobby
            form.save()
            context_container = LocationsListContextContainer(
                locations_list=Location.objects.get_locations_for_lobby(lobby)
            )
            context = context_container.get_context()
            print(context)
            return render(request, 'partials/locations_list.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
def select_location(request):
    if request.method == 'POST':
        location_id = request.POST.get('location_id')
        location = Location.objects.get_location_by_id(location_id)
        if location and Location.objects.is_user_has_access_to_location(request.user, location):
            request.session['current_location_id'] = location.id
            
            character_positions_context_container = CharacterPositionContextContainer(
                character_positions=CharacterPosition.objects.get_all_character_positions_in_location(location)
            )
            
            location_map_context_container = LocationMapContextContainer(
                current_location_id=location.id,
                current_location=location,
                rows_count=location.rows_count,
                cols_count=location.columns_count,
                characters_list=Location.objects.get_characters_in_location(location),
                character_position_context=character_positions_context_container
            )
            context = location_map_context_container.get_context()
            return render(request, 'partials/battle_map.html', context)
    return HttpResponseBadRequest("Location not found.")

@login_required
@lobby_id_in_session_required
@lobby_membership_required
def battlefield(request):    
    current_lobby_id = request.session.get('current_lobby_id')
    lobby = Lobby.objects.get_lobby_by_id(current_lobby_id)  
    current_location_id = request.session.get('current_location_id')
    
    characters_in_current_location = []
    locations_list = []
    selected_location = None
    rows_count = 0
    cols_count = 0
    move_character_form = None
    add_character_form = None
    add_npc_form = None
    add_user_form = AddUserToGroupForm(lobby=lobby)
    create_location_form = CreateLocationForm()

    locations_list = Location.objects.get_locations_for_lobby(lobby)
    if locations_list and not current_location_id:
        current_location_id = locations_list.first().id

    if current_location_id:
        selected_location = Location.objects.get_location_by_id(current_location_id)
        
        rows_count = selected_location.rows_count
        cols_count = selected_location.columns_count
        
        characters_in_current_location = Location.objects.get_characters_in_location(selected_location)        
        
        characters_available_to_move_for_user = None
        if LobbyRole.objects.user_has_role(request.user, lobby, DefaultRoles.GAME_MASTER):
            characters_available_to_move_for_user = characters_in_current_location
        else:        
            characters_available_to_move_for_user = Location.objects.get_characters_in_location_for_user(user=request.user, location=selected_location)
        
        move_character_form = MoveCharacterForm(available_characters=characters_available_to_move_for_user)    
        add_character_form = AddCharacterToGroupForm(lobby=lobby)
        add_npc_form = AddNPCToLobbyForm(lobby=lobby)
    
    character_positions_context_container = CharacterPositionContextContainer(
        character_positions=CharacterPosition.objects.get_all_character_positions_in_location(selected_location)
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
        current_lobby_id=current_lobby_id,
        current_lobby=lobby,
        locations_list=locations_list,
        users_list=Lobby.objects.get_users_in_lobby(lobby),
        move_character_form=move_character_form,
        add_character_form=add_character_form,
        add_npc_form=add_npc_form,
        add_user_form=add_user_form,
        create_location_form=create_location_form,
        location_map_context=location_context_container
    )
    context = battlefield_context_container.get_context()
    return render(request, 'battlefield.html', context)
    