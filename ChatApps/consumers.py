# chat/consumers.py
import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from CustomUser.models import CustomUser
from .models import ChatRoom, TextMessages
from django.shortcuts import get_object_or_404
from .models import ChatRoom
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": self.channel_name}))


def saving_messages_to_chat_room(chat_room, send_by_user, text_messages):
    new_text_msg_obj = TextMessages(
        users_room = chat_room,
        send_by = send_by_user,
        message_text = text_messages
    )
    new_text_msg_obj.save()

    return new_text_msg_obj


async def retrive_existing_messages(chat_room_obj):
    existing_text_message = await sync_to_async(TextMessages.objects.filter)(users_room=chat_room_obj)
    if await sync_to_async(existing_text_message.exists)():
        return await sync_to_async(list)(existing_text_message.values())
    else:
        return None




# SINGLE CHAT CONSUMERS -------------->>>

class SingleChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Getting user Id Where Message will be sent
        self.sent_to_user_id = self.scope["url_route"]["kwargs"]["user_id"]

       
        # Current Logged in user
        logged_in_user_details = self.scope["user"]
        self.send_by_user_id = logged_in_user_details.id
        # print(self.sent_to_user_id, self.send_by_user_id)

        first_user = await sync_to_async(get_object_or_404)(CustomUser, id=self.send_by_user_id)
        second_user = await sync_to_async(get_object_or_404)(CustomUser, id=self.sent_to_user_id)

        # Check if a ChatRoom already exists where these two users are present
        existing_chat_room = await sync_to_async( ChatRoom.objects.filter)(
            Q(first_user=first_user, second_user=second_user) |
            Q(first_user=second_user, second_user=first_user)
        )
 
        existing_room = await sync_to_async(existing_chat_room.first)()      
        if existing_room:
            self.user_chat_room_obj = existing_room
            self.users_common_chat_room_name = existing_room.room_name
        else:
            # If no ChatRoom exists, create a new one
            new_chat_room = await sync_to_async(ChatRoom.objects.create)(
                first_user=first_user,
                second_user=second_user,
                room_name= f"single_chat{self.send_by_user_id}-{self.sent_to_user_id}"
            )
            self.users_common_chat_room_name = new_chat_room.room_name
            self.user_chat_room_obj = new_chat_room



        # Join room group
        await self.channel_layer.group_add(self.users_common_chat_room_name, self.channel_name)
        # await self.channel_layer.group_add(self.send_by_user_chat_room, self.channel_name)

        await self.accept()


        existing_msg = await retrive_existing_messages(self.user_chat_room_obj)
        if existing_msg:
            await self.channel_layer.group_send(
            self.users_common_chat_room_name, {
                "type":"send.existing.message.to.websocket",
                "message": existing_msg

            },
            )


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.users_common_chat_room_name, self.channel_name)



    # Receive message from WebSocket
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        send_by_user_obj = await sync_to_async(get_object_or_404)(CustomUser, id=self.send_by_user_id)
        #saving message to database
        saved_message = await sync_to_async(saving_messages_to_chat_room)(self.user_chat_room_obj, send_by_user_obj, message)

        # Sent message to users room
        await self.channel_layer.group_send(
            self.users_common_chat_room_name, {
                "type": "chat.message", 
                "message": message,
                "send_by_user_id": self.send_by_user_id,
                "sent_to_user_id": self.sent_to_user_id
                }

        )

    # Receive message from room group
    async def chat_message(self, event):
        data = {"message": event["message"],
                "send_by_user_id": event["send_by_user_id"],
                "sent_to_user_id": event["sent_to_user_id"]
                }

        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    async def send_existing_message_to_websocket(self, event):
        data = {
            "message": event["message"],
        }

        await self.send(text_data=json.dumps(data))
