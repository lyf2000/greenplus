from collections import AsyncIterable

from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
import json, asyncio

# from .models import Message, Chat, Contact
# from .views import get_last_10_messages, get_user_contact, get_current_chat
from chat.models import Chat

User = get_user_model()


# TODO send case error

# async def add_chat(s, urls):
#     tasks = [s.channel_layer.group_add(
#         id,
#         s.channel_name
#     ) for id in urls]
#     await asyncio.wait(tasks)
#
#
# async def disc(s, urls):
#     tasks = [s.channel_layer.group_discard(
#         id,
#         s.channel_name
#     ) for id in urls]
#     await asyncio.wait(tasks)


# class ChatConsumer(AsyncJsonWebsocketConsumer):
#
#     async def connect(self):
#         user = self.scope['user']
#
#         # self.user_group_id = f'notify_user_{user.pk}'
#         # await self.channel_layer.group_add(
#         #     self.user_group_id,
#         #     self.channel_name
#         # )
#
#         chat_id_list = user.chats.all().values_list('id', flat=True)
#
#         self.chat_group_id_list = list([f'chat_{chat_id}' for chat_id in chat_id_list])
#
#         # await add_chat(self, self.chat_group_id_list)
#
#         await self.accept()
#
#     async def disconnect(self, code):
#         pass
#         # await disc(self, self.chat_group_id_list)
#
#         # await self.channel_layer.group_discard(
#         #     self.user_group_id,
#         #     self.channel_name
#         # )
#
#     async def receive_json(self, content):
#         print('recs', self, content)
#         command = content['command']
#         if command == 'join':
#             pass
#         elif command == 'leave':
#             pass
#         elif command == 'send':
#             await self.send_message(content['message'])
#         elif command == 'send_chat':
#             group = content['chat_id']
#             message_text = content['message']
#             await self.channel_layer.group_send(
#                 group,
#                 {
#                     'type': 'chat_message',
#                     'message': message_text,
#                     'group': group
#                 }
#             )
#         else:
#             await self.send_json({'error': 'What\'s the fucking wrong command??'})
#
#     async def send_message(self, message):
#         await self.send_json({'message': message})
#
#     async def chat_message(self, event):
#         # TODO check all is fine
#         message = event['message']
#         group = event['group']
#         m = ' '.join([group, message])
#         await self.send(text_data=json.dumps({'message': m}))


class NotifyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        self.user_group_id = f'notify_user_{user.pk}'

        await self.channel_layer.group_add(
            self.user_group_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.user_group_id,
            self.channel_name
        )

    async def receive_json(self, content):
        print('recs', self, content)
        command = content['command']
        if command == 'join':
            pass
        elif command == 'leave':
            pass
        elif command == 'send':
            await self.send_message(content['message'])
        elif command == 'send_chat':
            group = content['chat_id']
            message_text = content['message']
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'chat_message',
                    'message': message_text,
                    'group': group
                }
            )
        else:
            await self.send_json({'error': 'What\'s the fucking wrong command??'})

    # async def chat_join(self, room):
    #     self.rooms.append(room)

    async def send_message(self, message):
        await self.send_json({'message': message})

    async def chat_message(self, event):
        message = event['message']
        group = event['group']
        m = ' '.join([group, message])
        await self.send(text_data=json.dumps({'message': m}))
# class ChattConsumer(WebsocketConsumer):
#
#     def fetch_messages(self, data):
#         messages = get_last_10_messages(data['chatId'])
#         content = {
#             'command': 'messages',
#             'messages': self.messages_to_json(messages)
#         }
#         self.send_message(content)
#
#     def new_message(self, data):
#         user_contact = get_user_contact(data['from'])
#         message = Message.objects.create(
#             contact=user_contact,
#             content=data['message'])
#         current_chat = get_current_chat(data['chatId'])
#         current_chat.messages.add(message)
#         current_chat.save()
#         content = {
#             'command': 'new_message',
#             'message': self.message_to_json(message)
#         }
#         return self.send_chat_message(content)
#
#     def messages_to_json(self, messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result
#
#     def message_to_json(self, message):
#         return {
#             'id': message.id,
#             'author': message.contact.user.username,
#             'content': message.content,
#             'timestamp': str(message.timestamp)
#         }
#
#     commands = {
#         'fetch_messages': fetch_messages,
#         'new_message': new_message
#     }
#
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()
#
#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     def receive(self, text_data):
#         data = json.loads(text_data)
#         self.commands[data['command']](self, data)
#
#     def send_chat_message(self, message):
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     def send_message(self, message):
#         self.send(text_data=json.dumps(message))
#
#     def chat_message(self, event):
#         message = event['message']
#         self.send(text_data=json.dumps(message))
