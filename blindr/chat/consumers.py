import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from django.db.models import Q
from blindr.models import MatchesModel, UserModel, Message
from channels.db import database_sync_to_async
from .util import NativeNotifyAPI

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['url_route']['kwargs']['username']
        self.recipient_username = self.scope['url_route']['kwargs']['recipient_username']

        # Ensure that the sender is authenticated
        if self.sender is None:
            print(self.sender)
            await self.close()
        else:
            self.room_group_name = self.get_room_group_name(self.sender, self.recipient_username)

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        await self.accept()
        # await self.retrieve_and_send_messages()

    
    async def retrieve_and_send_messages(self):
        match = await self.get_matches_from_name(self.sender, self.recipient_username)
        messages = await self.get_messages(match)
        #input()
        gifted_chat_messages = []
        for message in messages:
            # input("PAUSING________")
            gifted_chat_messages.append(await message.to_gifted_chat_message())
        self.send_json({
            'type': 'retrieve_messages',
            'messages': gifted_chat_messages,
        })

    @database_sync_to_async
    def get_messages(self, match):
        messages = Message.objects.filter(match=match).order_by('timestamp')
        return messages

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        message_content = data['text']

        match = await self.get_matches_from_name(self.sender, self.recipient_username)
        sender = await self.get_user_by_id(self.sender)

        new_message = await self.create_message(match, sender, message_content)
        print(NativeNotifyAPI(   10776, "bMAL30KDs4RJB8RaFqimlb" ).send_notificationToSpecUser(self.recipient_username, sender.name, message_content))
        # Broadcast the message to all participants
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': new_message.to_gifted_chat_message(),  # Use the to_gifted_chat_message method
                'user': self.sender,
                'recipient': self.recipient_username,
            }
        )

    @database_sync_to_async
    def create_message(self, match, sender, content):
        print("MAKING MESSAGE")
        return Message.objects.create(match=match, sender=sender, content=content)

    @database_sync_to_async
    def get_user_by_id(self, sender):
        return UserModel.objects.get(userId=sender)

    @sync_to_async
    def get_matches_from_name(self, u1, u2):
        try:
            match = MatchesModel.objects.get(
                Q(user_1=u1, user_2=u2) |
                Q(user_1=u2, user_2=u1)
            )
            return match
        except MatchesModel.DoesNotExist:
            return None

    async def chat_message(self, event):
        message = event['message']
        await self.send_json({
            'type': 'chat_message',
            'message': message,
            'sender_username': event['user'],
            'recipient': event['recipient']
        })

    @staticmethod
    def get_room_group_name(sender_username, recipient_username):
        sorted_usernames = sorted([sender_username, recipient_username])
        return f'private_chat_{sorted_usernames[0]}_{sorted_usernames[1]}'
