import json
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from battlefield.utils.contexts.character_position_context import CharacterPositionContextContainer
from battlefield.utils.contexts.location_map_context import LocationMapContextContainer
from battlefield.utils.managers.character_position_manager import CharacterPositionManager
from battlefield.utils.managers.location_manager import LocationManager
from characters.utils.managers.character_manager import CharacterManager
from groups.utils.managers.group_manager import GroupManager
from battlefield.utils.ruler import ruler

class MoveCharacterConsumer(WebsocketConsumer):
    def connect(self):
        #Initiates once when user connects
        self.user = self.scope["user"]
        self.group_id = self.scope['url_route']['kwargs']['current_group_id']
        self.group = GroupManager.get_group_by_id(self.group_id)
        self.current_location_id = None
        self.chatroom_name = f"group_{self.group_id}"
        
        # Add user to the websocket group
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        
        # Accept the connection
        self.accept()

    def disconnect(self, close_code):
        #Called when the socket closes
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

    def receive(self, text_data):
        #Called when a message is received from the WebSocket
        text_data_json = json.loads(text_data)
        new_pos_row = text_data_json.get('row')
        new_pos_column = text_data_json.get('column')
        character_id = text_data_json.get('name')
        self.current_location_id = text_data_json.get('current_location_id')
        current_location = LocationManager.get_location_by_id(self.current_location_id)

        character = CharacterManager.get_character_by_id(character_id)
        character_position = CharacterPositionManager.get_character_position_in_location(
            character,
            current_location
        )

        requested_distance = ruler(character_position.column, character_position.row, new_pos_column, new_pos_row)
        allowed_distance = character.movement_speed / 5
        if allowed_distance >= requested_distance:
            if not CharacterPositionManager.is_position_occupied(current_location, new_pos_row, new_pos_column):
                CharacterPositionManager.move_character(
                    character,
                    current_location,
                    new_pos_row,
                    new_pos_column
                )

                event = {
                    'type': 'message_handler',
                }

                async_to_sync(self.channel_layer.group_send)(
                    self.chatroom_name,
                    event
                )

    def message_handler(self, event):
        location = LocationManager.get_location_by_id(self.current_location_id)
        characters = LocationManager.get_characters_in_location(location)
        
        character_positions_context_container = CharacterPositionContextContainer(
            character_positions=CharacterPositionManager.get_all_character_positions_in_location(location)
        )
        
        context_container = LocationMapContextContainer(
            current_location_id=self.current_location_id,
            current_location=location,
            rows_count=location.rows_count,
            cols_count=location.columns_count,
            characters_list=characters,
            character_position_context=character_positions_context_container
        )
        
        context = context_container.get_context()
        html = render_to_string('partials/battle_map.html', context)
        self.send(text_data=html)