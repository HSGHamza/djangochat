import json
from channels.generic.websocket import WebsocketConsumer
from chat.models import ActiveConnection
from accounts.models import User


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        message = json.loads(text_data)
        reciever = User.objects.get(reciever=message.get("reciever_id"))
        reciever_connection = ActiveConnection.objects.get(user=reciever)
        reciever_channel_name = reciever_connection.channel_name
        if not ActiveConnection.objects.filter(channel_name=self.channel_name).exists:
            ActiveConnection.objects.create(
                channel_name=self.channel_name, 
                user=User.objects.get(id=message.get("sender_id"))
            )

        self.channel_layer.send(reciever_channel_name, message.get("message"))
        # self.send(text_data=json.dumps({"message": message}))
