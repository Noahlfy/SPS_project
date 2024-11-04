import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Rejoindre le groupe WebSocket
        await self.channel_layer.group_add("data_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe WebSocket
        await self.channel_layer.group_discard("data_group", self.channel_name)

    async def send_data(self, event):
        # Récupère les données envoyées par DataHandler
        data = event["data"]
        print("Sending data to frontend")  # Pour voir les données côté serveur

        # Envoie les données au frontend
        await self.send(text_data=json.dumps(data))
