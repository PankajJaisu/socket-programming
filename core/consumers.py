

from channels.generic.websocket import WebsocketConsumer 
from asgiref.sync import async_to_sync
import json
import asyncio

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        # self.group_name = 'room_%s' % self.room_name
        self.group_name = f'room_{self.room_name}' 
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.scope['session'].setdefault('messages', [])
        
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
    def receive(self,text_data):
        data = json.loads(text_data)
        payload = {'message':data.get('message'),'sender':data.get('sender')}
        self.scope['session']['messages'].append(data.get('message'))
        self.scope['session'].save()


        async_to_sync(self.channel_layer.group_send)(
            f'room_{self.room_name}',{
                'type':'send_message',
                'value':json.dumps(payload)
            }
        )
    def disconnect(self,close_code):
       
        pass 
    def send_message(self,text_data):
        
        data = text_data.get('value')
        self.send(text_data=json.dumps({
            'payload':data
        }))


    def get_all_messages(self):
        # Retrieve all messages from the session
        session_data = self.scope['session']
        expiry_date = session_data.get('_session_expiry')
        session_key = session_data.session_key
        print(f"Session Key: {session_key}, Expiry Date: {expiry_date}")
        return session_data.get('messages', [])

    def fetch_messages(self, event):
        # Send stored messages to the user upon connection
        messages = self.get_all_messages()
        self.send(text_data=json.dumps({'type': 'chat.messages', 'messages': messages}))