import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.group_name = "chat_%s" % self.chat_box_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message,
                "username": username,
            },
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
