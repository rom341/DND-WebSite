import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from battlefield.models import Group
from battlefield.utils.model_managers.group_manager import GroupManager
from battlefield.utils.ruler import ruler

class MoveCharacterConsumer(WebsocketConsumer):
    def connect(self):
        #Initiates once when user connects
        self.user = self.scope["user"]
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group = GroupManager.get_group_by_id(self.group_id)
        self.chatroom_name = f"group_{self.group_id}"
        print(f"User {self.user} connected to websocket group {self.group_id}")
        
        # Add user to the websocket group
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        
        # Accept the connection
        self.accept()

    def disconnect(self, close_code):
        #Called when the socket closes
        print(f"User {self.user} disconnected from group {self.group_id}")
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

    def receive(self, text_data):
        #Called when a message is received from the WebSocket
        text_data_json = json.loads(text_data)
        print(f"Received message: {text_data_json}")
        
        new_pos_x = text_data_json.get('position_x')
        new_pos_y = text_data_json.get('position_y')
        character_id = text_data_json.get('name')

        # Find the character to move
        character = GroupManager.get_characters_in_group(self.group).filter(id=character_id).first()
        if not character:
            print(f"Character with ID {character_id} not found in group {self.group_id}")
            return 

        # Проверка на допустимое расстояние перемещения
        requested_distance = ruler(character.position_x, character.position_y, new_pos_x, new_pos_y)
        allowed_distance = character.movement_speed / 5
        print('++++++++++++++++++++++++++')
        print(requested_distance,allowed_distance)
        if allowed_distance >= requested_distance:
            # Проверка свободна ли позиция            
            if not GroupManager.is_position_occupied(self.group, new_pos_x, new_pos_y):
                character.move_to(new_pos_x, new_pos_y)
                print(f"Character {character.name} moved to ({new_pos_x}, {new_pos_y})")

                event = {
                    'type': 'message_handler',
                    #'character': character
                }

                async_to_sync(self.channel_layer.group_send)(
                    self.chatroom_name,
                    event
                )

    def message_handler(self, event):
        characters = GroupManager.get_characters_in_group(self.group)
        context = {
            'rows_count': 10,
            'cols_count': 5,
            'rows_range': range(10),
            'cols_range': range(5),
            'characters': characters,
        }
        html = render_to_string('partials/battle_map.html', context)
        self.send(text_data=html)