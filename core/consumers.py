

from channels.generic.websocket import WebsocketConsumer 
from asgiref.sync import async_to_sync
import json

class TestConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = 'test_consumer'
        self.room_group_name = 'test_consumer_group'

        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.room_group_name
        )

        # Accept the WebSocket connection
        self.accept()

        # Send a message to the client upon connection
        self.send(text_data=json.dumps({'status': 'Hello this is Pankaj'}))
       

    def receive(self, text_data):
        # Process the received message (add your logic here)
        print("Received message:", text_data)

    def disconnect(self, close_code):
        # Remove the consumer from the group when the WebSocket is closed
        print('disconnect::')