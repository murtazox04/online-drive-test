import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .serializers import AvailableDriverSerializer
from .services import DriverService


class AvailableDriversConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "available_drivers"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        drivers = await self.get_available_drivers()
        await self.send(
            text_data=json.dumps({"type": "driver_list", "drivers": drivers})
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "get_drivers":
            drivers = await self.get_available_drivers()
            await self.send(
                text_data=json.dumps({"type": "driver_list", "drivers": drivers})
            )

    async def driver_update(self, event):
        await self.send(
            text_data=json.dumps({"type": "driver_update", "drivers": event["drivers"]})
        )

    @database_sync_to_async
    def get_available_drivers(self):
        drivers = DriverService.get_available_drivers()
        serializer = AvailableDriverSerializer(drivers, many=True)
        return serializer.data
