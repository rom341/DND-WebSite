import json
from channels.generic.websocket import WebsocketConsumer

class BattlefieldConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"Received message: {text_data_json}")