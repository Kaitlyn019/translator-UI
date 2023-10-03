import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
#from google.cloud import translate_v2 as translate
from deep_translator import GoogleTranslator

#translate_client = translate.Client()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        isFinal = text_data_json['isFinal']
        #result = translate_client.translate(message, target_language='zh')
        
        translated = GoogleTranslator(source='en', target='zh-CN').translate(text=message)
        print (translated)
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'isFinal': isFinal,
                'translated': translated
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'translated': event['translated'],
            'isFinal': event['isFinal']
        }))
