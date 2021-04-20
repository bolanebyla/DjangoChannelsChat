import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from . import models


@database_sync_to_async
def get_user_chat(pk, user):
    chat = models.Chat.objects.get(id=pk, clients=user)
    return chat


class ChatConsumer(AsyncWebsocketConsumer):
    chat_group_name = None
    chat_id = None

    async def connect(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")

        self.chat_id = self.scope['url_route']['kwargs']['room_id']

        try:
            chat = await get_user_chat(pk=self.chat_id, user=self.scope['user'])
            self.chat_group_name = f'chat_{chat.id}'

            # Join room group
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name
            )
            await self.accept()

        except ObjectDoesNotExist:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = str(self.scope['user'])
        user = {
            'username': username
        }

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))
