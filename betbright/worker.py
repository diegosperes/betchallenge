import asyncio
from bson.json_util import loads

from betbright.server import app
from betbright.models import message, event
from betbright.models.message import (
    generate_message, SCHEDULED_STATUS_MESSAGE, PROCESSED_STATUS_MESSAGE
)
from betbright.broker import Broker


class Worker:
    def __init__(self, loop):
        self.loop = loop

    async def setup(self):
        self.broker = await Broker(self.loop).connect()
        app.broker = self.broker

    async def run(self, loop):
        await self.setup()
        await self.execute()
        await self.loop.call_soon(self.execute())

    async def execute(self):
        data = await self._get_scheduled_message()
        query = {"id": data['event']['id']}
        document = await event.find(unique=True, **query)
        if document:
            await event.update(data, query)
        else:
            await event.insert(data['event'])
        await self._update_message_status(data, PROCESSED_STATUS_MESSAGE)

    async def _get_scheduled_message(self):
        queue = await self.broker.get_queue('message')
        event = await queue.get(timeout=5)
        with event.process():
            data = loads(event.body.decode())
            data = await self._update_message_status(data, SCHEDULED_STATUS_MESSAGE)
            await message.delete_cache(data)
            return data

    async def _update_message_status(self, data, status):
        query = {'_id': data['_id']}
        data = generate_message(data, status)
        await message.update(data, query)
        return data


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    worker = Worker(loop)
    loop.run_until_complete(worker.run())
    loop.close()
