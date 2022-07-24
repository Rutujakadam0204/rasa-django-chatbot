# # chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import requests


# class ChatFaqConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = 'chatbot'
#         self.user = self.scope["user"]
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         await(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': "Hello, "+str(self.user)
#             }
#         )
        
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         # Send message to room group
#         await(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#         if self.scope['user'].username:
#             # await self.save_question(message)
#             await self.answer_question(message)
#         else:
#             pass
        
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

#     @database_sync_to_async
#     def answer_question(self, message):
#         a=transform_message(message)
#         message = 'message'
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#         return 0


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        if self.scope['user'].username:
            # await self.save_question(message)
            await self.answer_question(message)
        else:
            pass

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def answer_question(self, message):
        print(message)
        payload = json.dumps({"sender": "Rasa","message": message})
        headers = {'Content-type':'application/json', 'Accept':'text/plain'}
        response = requests.request("POST", url="http://localhost:5005/webhooks/rest/webhook", headers=headers, data=payload)
        response=response.json()
        resp=[]
        for i in range(len(response)):
            try:
                resp.append(response[i]['text'])
            except:
                continue
        message = resp
        print(message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        return 0
