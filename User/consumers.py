import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from crum import get_current_user
from User.models import Message, MyUser, Room as Room_model

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        logging.info('self.room_name: %s', self.room_name)
        self.roomGroupName = 'chat_%s' % self.room_name
        logging.info('self.roomGroupName: %s', self.roomGroupName)
        
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
        
    async def receive(self, text_data):
        logging.info("Received message: %s", text_data)  # Debugging statement
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        logging.info('message: %s', message)
        username = text_data_json["username"]
        logging.info('username: %s', username)
        room_name = text_data_json["room_name"]
        logging.info('room_name: %s', room_name)
        
        await self.save_message(message, username, room_name)     

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "room_name": room_name,
            }
        )
        
    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))
    
    # @sync_to_async
    # def save_message(self, message, username, room_name):
    #     print('room_name: ', room_name)
    #     print("---------in_function------",username)
    #     user_obj = MyUser.objects.get(username=username) 
    #     print('user_obj: ', user_obj)
    #     user1_username, user2_username = room_name.split('_')
        
    #     # Retrieve the user objects from the database
    #     user1 = MyUser.objects.get(username=user1_username)
    #     user2 = MyUser.objects.get(username=user2_username)
    #     print('user1: ', user1)
    #     print('user2: ', user2)
        
    #     # Check which user is the logged-in user
    #     if user_obj == user1:
    #         reciver=user_obj
    #     else:
    #         sender= user2
    #     room_obj=Room_model.objects.get(name=room_name)
    #     Message.objects.create(user=user_obj, room=room_obj, content=message,sender=sender ,receiver=reciver)  # Create the message object
    @sync_to_async
    def save_message(self, message, username, room_name):
        print('room_name: ', room_name)
        print("---------in_function------",username)
        user_obj = MyUser.objects.get(username=username) 
        user1_username = room_name.split('_')[1]  # Splitting by underscore and getting the second part
        user2_username = room_name.split('_')[2]   # Limiting the split to only 1 occurrence
        print('user1_username: ', user1_username)
        print('user2_username: ', user2_username)
        
        # Retrieve the user objects from the database
        user1 = MyUser.objects.get(username=user1_username)
        user2 = MyUser.objects.get(username=user2_username)
        print('user1: ', user1)
        print('user2: ', user2)
        
        # Check which user is the logged-in user
        if user_obj.username == user1.username:
            receiver = user2
            sender = user1
        else:
            receiver = user1
            sender = user2
            
        
        room_obj = Room_model.objects.get(name=room_name)
        Message.objects.create(user=user_obj, room=room_obj, content=message, sender=sender, receiver=receiver)
