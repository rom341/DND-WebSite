from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from core.managers.SessionManager import SessionManager
from lobby.forms.add_character_to_lobby_form import AddCharacterToGroupForm
from lobby.forms.add_npc_to_lobby_form import AddNPCToLobbyForm
from lobby.forms.add_user_to_lobby_form import AddUserToLobbyForm
from location.models import CharacterPosition, Location
from battlefield.utils.common_request_helper import CommonRequestHelper
from battlefield.utils.contexts.battlefield_context import BattleieldContextContainer
from battlefield.utils.contexts.character_position_context import CharacterPositionContextContainer
from battlefield.utils.contexts.location_map_context import LocationMapContext
from battlefield.utils.decorators import game_master_required
from characters.models import Character, EntityBase
from lobby.models import DefaultRoles, Lobby
from service.lobby import actions
from service.role import selectors as RoleSelectors

# Create your views here.
@login_required
def lobby(request):
    active_user = request.user    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        try:
            with transaction.atomic(): # Ensure that the whole function is atomic (all-or-nothing)
                if action == 'select': # lobby selected
                    lobby_id = request.POST.get('lobby_id')
                elif action == 'create': # new lobby created
                    new_lobby_name = request.POST.get('lobby_name')
                    new_lobby = actions.create_lobby_with_gm(active_user, new_lobby_name)
                    lobby_id = new_lobby.id
                    
                if lobby_id:
                    session_manager = SessionManager.get_session_manager(request=request)
                    session_manager.set_current_lobby_id(lobby_id=lobby_id)
                    
                    return redirect(reverse('battlefield'))
                else:
                    messages.error(request, "Lobby is not valid")
                    
        except Exception as e:
            messages.error(request, f"Unknown error while operating lobby selection page: {str(e)}")
            return redirect(reverse('lobby'))
        
    lobby = Lobby.objects.get_lobbys_with_user(active_user)   
    data = {
        'lobbys': lobby,
    }

    return render(request, 'lobby.html', data)

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
                actions.add_user_as_player_to_lobby(selected_user, current_lobby)
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