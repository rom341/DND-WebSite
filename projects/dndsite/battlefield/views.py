from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import redirect, render
from base.managers.SessionManager import SessionManager
from battlefield.forms.add_character_to_lobby_form import AddCharacterToGroupForm
from battlefield.forms.add_npc_to_lobby_form import AddNPCToLobbyForm
from battlefield.forms.add_user_to_lobby_form import AddUserToLobbyForm
from battlefield.forms.create_location_form import CreateLocationForm
from battlefield.forms.move_character_form import MoveCharacterForm
from battlefield.models import CharacterPosition, Location
from battlefield.utils.common_request_helper import CommonRequestHelper
from battlefield.utils.contexts.battlefield_context import BattleieldContextContainer
from battlefield.utils.contexts.character_position_context import CharacterPositionContextContainer
from battlefield.utils.contexts.location_map_context import LocationMapContext
from battlefield.utils.contexts.locations_list_context import LocationsListContext
from battlefield.utils.decorators import game_master_required, lobby_id_in_session_required, lobby_membership_required
from characters.forms.heal_character_form import HealCharacterForm
from characters.models import Character, EntityBase
from lobby.models import DefaultRoles, Lobby, LobbyRole


# Create your views here.
@login_required
@game_master_required
def add_user_to_lobby(request):
    if request.method == 'POST':
        session_manager = SessionManager.get_session_manager(request=request)
        current_lobby = session_manager.get_current_lobby()
        if current_lobby:
            form = AddUserToLobbyForm(request.POST, lobby=current_lobby)
            if form.is_valid():
                selected_user_id = request.POST.get('user_id')
                selected_user = User.objects.get(id=selected_user_id)
                Lobby.objects.add_user_to_lobby(selected_user, current_lobby)
                return CommonRequestHelper.get_updated_user_list_widget(request, current_lobby)
    
    return HttpResponseBadRequest("Invalid request method.")

@login_required
@game_master_required
def add_character_to_lobby(request):
    if request.method == 'POST':
        session_manager = SessionManager.get_session_manager(request=request)
        lobby = session_manager.get_current_lobby()
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
                location_context_container = LocationMapContext(
                    current_locationd=location,
                    rows_count=location.rows_count,
                    cols_count=location.columns_count,
                    character_positions=character_positions_context_container.character_positions
                )
                context_container = BattleieldContextContainer(
                    current_lobby=lobby,
                    location_map_context=location_context_container,
                    add_character_form=form
                )
                context = context_container.get_context()
                return render(request, 'partials/battle_map.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")

@login_required
def heal_character(request):
    if request.method == 'POST':
        session_manager = SessionManager.get_session_manager(request=request)
        lobby = session_manager.get_current_lobby()
        current_location = session_manager.get_current_location()
        characters_available_for_current_user = Character.objects.get_characters_available_for_user_in_location(user=request.user, location=current_location)

        form = HealCharacterForm(request.POST, available_characters=characters_available_for_current_user)
        if form.is_valid():
            character = form.cleaned_data.get('character')
            heal_value = form.cleaned_data.get('health_value')
            heal_type = form.cleaned_data.get('heal_action_type')
            Character.objects.change_health(character=character, heal_value=heal_value, heal_type=heal_type)
            return HttpRequest("Successfull")

        return HttpResponseBadRequest("Failed")

@login_required
@game_master_required
def add_npc_to_lobby(request):
    if request.method == 'POST':
        session_manager = SessionManager.get_session_manager(request=request)
        lobby = session_manager.get_current_lobby()
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
                location_context_container = LocationMapContext(
                    current_location=location,
                    rows_count=location.rows_count,
                    cols_count=location.columns_count,
                    character_positions=character_positions_context_container.character_positions
                )
                context_container = BattleieldContextContainer(
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
        session_manager = SessionManager.get_session_manager(request=request)
        lobby = session_manager.get_current_lobby()
        form = CreateLocationForm(request.POST)
        if form.is_valid():
            form.instance.lobby = lobby
            form.save()
            context = LocationsListContext(
                locations_list=Location.objects.get_locations_for_lobby(lobby)
            )
            return render(request, 'partials/locations_list.html', context.to_dict())
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
def select_location(request):
    if request.method == 'POST':
        session_manager = SessionManager.get_session_manager(request=request)
        location_id = session_manager.get_current_location_id()
        location = session_manager.get_current_location()
        if location and Location.objects.is_user_has_access_to_location(request.user, location):
            request.session['current_location_id'] = location.id
            
            character_positions_context_container = CharacterPositionContextContainer(
                character_positions=CharacterPosition.objects.get_all_character_positions_in_location(location)
            )
            
            location_map_context_container = LocationMapContext(
                current_location=location,
                rows_count=location.rows_count,
                cols_count=location.columns_count,
                character_positions=character_positions_context_container.character_positions
            )
            context = location_map_context_container.to_dict()

            session_manager.set_current_location_id(location_id=location_id)
            return render(request, 'partials/battle_map.html', context)
    return HttpResponseBadRequest("Location not found.")

@login_required
@lobby_id_in_session_required
@lobby_membership_required
def battlefield(request:  HttpRequest):  
    session_manager = SessionManager.get_session_manager(request=request)
    lobby = session_manager.get_current_lobby()
    current_location_id = session_manager.get_current_location_id()
    current_location = session_manager.get_current_location()
    
    characters_in_current_location = []
    locations_list = []
    selected_location = None
    rows_count = 0
    cols_count = 0
    move_character_form = None
    add_character_form = None
    add_npc_form = None
    add_user_form = AddUserToLobbyForm(lobby=lobby)
    heal_character_form = None
    create_location_form = CreateLocationForm()

    locations_list = Location.objects.get_locations_for_lobby(lobby)
    if locations_list and not current_location_id:
        current_location_id = locations_list.first().id
        current_location = locations_list.first()

    if current_location_id:
        selected_location = Location.objects.get_location_by_id(current_location_id)
        
        rows_count = selected_location.rows_count
        cols_count = selected_location.columns_count
        
        characters_in_current_location = Location.objects.get_characters_in_location(selected_location)        
        
        characters_available_for_current_user = Character.objects.get_characters_available_for_user_in_location(user=request.user, location=current_location)

        move_character_form = MoveCharacterForm(available_characters=characters_available_for_current_user)
        heal_character_form = HealCharacterForm(available_characters=characters_available_for_current_user)
        add_character_form = AddCharacterToGroupForm(lobby=lobby)
        add_npc_form = AddNPCToLobbyForm(lobby=lobby)
    
    character_positions_context_container = CharacterPositionContextContainer(
        character_positions=CharacterPosition.objects.get_all_character_positions_in_location(selected_location)
    )
    
    location_context_container = LocationMapContext(
        current_location=selected_location,
        rows_count=rows_count,
        cols_count=cols_count,
        character_positions=character_positions_context_container.character_positions
    )
    
    battlefield_context_container = BattleieldContextContainer(
        current_lobby=lobby,
        locations_list=locations_list,
        users_list=Lobby.objects.get_users_in_lobby(lobby),
        move_character_form=move_character_form,
        add_character_form=add_character_form,
        add_npc_form=add_npc_form,
        add_user_form=add_user_form,
        create_location_form=create_location_form,
        heal_character_form=heal_character_form,
        location_map_context=location_context_container
    )
    context = battlefield_context_container.get_context()
    session_manager.set_current_location_id(location_id=current_location_id)
    return render(request, 'battlefield.html', context)
    