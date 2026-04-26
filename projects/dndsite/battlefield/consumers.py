import json
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from location.models import Location
from battlefield.serializers import LocationSerializer
from characters.models import Character, CharacterPosition
from battlefield.utils.ruler import ruler
from lobby.models import Lobby
from django.utils.safestring import mark_safe

class MoveCharacterConsumer(WebsocketConsumer):
    def connect(self):
        #Initiates once when user connects
        self.user = self.scope["user"]
        self.lobby_id = self.scope['url_route']['kwargs']['current_lobby_id']
        self.lobby = Lobby.objects.get_lobby_by_id(self.lobby_id)
        self.current_location_id = None
        self.chatroom_name = f"lobby_{self.lobby_id}"
        
        # Add user to the websocket lobby
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
        current_location = Location.objects.get_location_by_id(self.current_location_id)

        character = Character.objects.get_character_by_id(character_id)
        character_position = CharacterPosition.objects.get_character_position_in_location(
            character=character,
            location=current_location
        )
        requested_distance = ruler(character_position.column, character_position.row, new_pos_column, new_pos_row)
        allowed_distance = character.movement_speed / 5
        if allowed_distance >= requested_distance:
            if not CharacterPosition.objects.is_position_occupied(current_location, row=new_pos_row, column=new_pos_column):
                
                CharacterPosition.objects.move_character(
                    character=character,
                    location=current_location,
                    new_row=new_pos_row,
                    new_column=new_pos_column
                )

                event = {
                    'type': 'send_map_update', 
                    'location_id': self.current_location_id 
                }

                async_to_sync(self.channel_layer.group_send)(
                    self.chatroom_name,
                    event
                )
            else:
                self.send_error("Position ocupied")
        else:
            self.send_error("Not enough movement speed")

    def send_map_update(self, event):
        current_location_id = event.get('location_id')
        if not current_location_id:
            return
            
        location = Location.objects.get_location_by_id(current_location_id)
        #characters = Location.objects.get_characters_in_location(location)
        
        # character_positions = CharacterPosition.objects.get_all_character_positions_in_location(location)
        # character_positions_context_container = CharacterPositionContextContainer(
        #     character_positions=character_positions
        # )
        
        # context_container = LocationMapContext(
        #     current_location=location,
        #     rows_count=location.rows_count,
        #     cols_count=location.columns_count,
        #     character_positions=character_positions_context_container.character_positions
        # )
        
        # context = context_container.to_dict()
        # battle_map_html = render_to_string('partials/battle_map.html', context)
        # response_html = f"""
        # <div id="battle-map-container" class="col-10">
        #     {battle_map_html}
        # </div>
        # """
        #self.send(text_data=response_html)
        #d = context_container.to_dict_full()
        # self.send(text_data=json.dumps(d))
        serializer_loc = LocationSerializer(location)
        s_loc = json.dumps(serializer_loc.data)
        self.send(text_data=s_loc)

    def send_error(self, message: str):
        message_html = f'<div class="alert alert-danger p-1 small">Error: {message}</div>'
        context: dict[str, any] = {
            "extra_properties": mark_safe('hx-swap-oob="beforeend"'),
            "message": mark_safe(message_html),
        }
        html = render_to_string('notification_container.html', context)
        
        self.send(text_data=html)