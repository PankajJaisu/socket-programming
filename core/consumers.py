

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



active_users = {} 
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        # self.group_name = 'room_%s' % self.room_name
        self.group_name = f'room_{self.room_name}' 
        self.user_id = self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()
       

        async_to_sync(self.channel_layer.group_send)(
            f'room_{self.room_name}',{
                'type':'send_message',
                'value':json.dumps({'status':'online'})
            }
        )

        self.send(text_data=json.dumps({
            'payload':'connected'
        }))

        active_users.setdefault(self.user_id, [])

    def receive(self,text_data):
        data = json.loads(text_data)
        payload = {'message':data.get('message'),'sender':data.get('sender')}

        async_to_sync(self.channel_layer.group_send)(
            f'room_{self.room_name}',{
                'type':'send_message',
                'value':json.dumps(payload)
            }
        )
        active_users[self.user_id].append(data.get('message'))
        print("\n\n active_user::",active_users)

    def disconnect(self,close_code):
        active_users.pop(self.user_id, None)
        print(active_users)

    def send_message(self,text_data):
        print(type(text_data))
        data = text_data.get('value')
        self.send(text_data=json.dumps({
            'payload':data
        }))

    async def fetch_messages(self, event):

        # Send stored messages to the user upon connection

        messages = active_users.get(self.user_id, [])

        await self.send(text_data=json.dumps({'type': 'chat.messages', 'messages': messages}))


