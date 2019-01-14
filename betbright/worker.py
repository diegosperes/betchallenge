import asyncio
import logging
from bson.json_util import loads
from aio_pika.exceptions import QueueEmpty

from betbright.application import app, setup
from betbright.models import message, event
from betbright.models.message import (
    generate_message, SCHEDULED_STATUS_MESSAGE, PROCESSED_STATUS_MESSAGE
)


class Worker:
    def __init__(self, loop):
        self.loop = loop

    async def setup(self):
        await setup(app, self.loop)
        self.broker = app.broker

    async def run(self, loop):
        await self.setup()
        await self._execute()

    async def execute(self):
        data = await self._get_scheduled_message()
        if not data:
            return

        query = {"id": data['event']['id']}
        document = await event.find(unique=True, **query)
        if document:
            await event.update(data['event'], query)
        else:
            await event.insert(data['event'])
        await self._update_message_status(data, PROCESSED_STATUS_MESSAGE)

    async def _get_scheduled_message(self):
        try:
            queue = await self.broker.get_queue('message')
            event = await queue.get(timeout=5)
            with event.process():
                data = loads(event.body.decode())
                data = await self._update_message_status(data, SCHEDULED_STATUS_MESSAGE)
                await message.delete_cache(data)
                return data
        except QueueEmpty:
            pass

    async def _update_message_status(self, data, status):
        query = {'_id': data['_id']}
        data = generate_message(data, status)
        await message.update(data, query)
        return data

    async def _execute(self):
        try:
            await self.execute()
        except Exception as exception:
            logging.error(exception)
        self.loop.create_task(self._execute())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    worker = Worker(loop)
    loop.create_task(worker.run(loop))
    loop.run_forever()
    loop.close()
