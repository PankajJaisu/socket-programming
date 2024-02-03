

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

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        # self.group_name = 'room_%s' % self.room_name
        self.group_name = f'room_{self.room_name}' 
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()
        # data = {'type':'connected'}

        async_to_sync(self.channel_layer.group_send)(
            f'room_{self.room_name}',{
                'type':'send_message',
                'value':json.dumps({'status':'online'})
            }
        )

        self.send(text_data=json.dumps({
            'payload':'connected'
        }))
    def receive(self,text_data):
        data = json.loads(text_data)
        payload = {'message':data.get('message'),'sender':data.get('sender')}

        async_to_sync(self.channel_layer.group_send)(
            f'room_{self.room_name}',{
                'type':'send_message',
                'value':json.dumps(payload)
            }
        )
    def disconnect(self,close_code):
        pass

    def send_message(self,text_data):
        print(type(text_data))
        data = text_data.get('value')
        self.send(text_data=json.dumps({
            'payload':data
        }))