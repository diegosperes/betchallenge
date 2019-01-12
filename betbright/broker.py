import asyncio
import aio_pika

from betbright.config import settings


class Broker:
    def __init__(self, loop=None):
        self.loop = loop if loop else asyncio.get_event_loop()

    async def connect(self):
        uri = settings['broker']['uri']
        self.connection = await aio_pika.connect_robust(uri, loop=self.loop)
        self.channel = await self.connection.channel()
        return self

    def get_channel(self):
        return self.channel

    async def get_queue(self, name):
        return await self.channel.declare_queue(name, auto_delete=False)

    async def disconnect(self):
        await self.connection.close()
