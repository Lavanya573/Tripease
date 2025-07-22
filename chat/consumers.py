from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
from .models import ChatSession, ChatMessage
from asgiref.sync import sync_to_async

class SupportChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'chat_{self.session_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data.get('type') == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'sender_id': self.scope['user'].id,
                    'sender_username': self.scope['user'].username,
                }
            )
            return
        message = data.get('message')
        sender_id = self.scope['user'].id
        message_type = data.get('message_type', 'text')
        file_url = data.get('file_url')
        # Save message to DB
        await self.save_message(self.session_id, sender_id, message, message_type, file_url)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'sender_username': self.scope['user'].username,
                'message_type': message_type,
                'file_url': file_url,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'message_type': event['message_type'],
            'file_url': event['file_url'],
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
        }))

    @sync_to_async
    def save_message(self, session_id, sender_id, message, message_type, file_url):
        session = ChatSession.objects.get(pk=session_id)
        sender = User.objects.get(pk=sender_id)
        ChatMessage.objects.create(
            session=session,
            sender=sender,
            message=message or '',
            message_type=message_type,
            file=file_url if message_type == 'file' else None
        ) 