import aio_pika
from datetime import datetime
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

from betbright.application import app
from betbright.models.model import Model


SENT_STATUS_MESSAGE = 'sent'
SCHEDULED_STATUS_MESSAGE = 'scheduled'
PROCESSED_STATUS_MESSAGE = 'processed'

_template_key = 'message_{_id}'
_queue = 'message'


def generate_message(data, status):
    if status == SCHEDULED_STATUS_MESSAGE:
        data['scheduled_at'] = datetime.now()
    elif status == PROCESSED_STATUS_MESSAGE:
        data['@uri'] = '/api/match/{0}'.format(data['event']['id'])
        data['processed_at'] = datetime.now()

    return {
        "_id": data.get('_id', ObjectId()),
        "@uri": data.get('@uri'),
        "event": data['event'],
        "status": status,
        "sent_at": data.get('sent_at', datetime.now()),
        "scheduled_at": data.get('scheduled_at'),
        "processed_at": data.get('processed_at'),
    }


class Message(Model):
    @property
    def collection(self):
        return app.mongo['message']

    async def find(self, **kwargs):
        _id = kwargs.get('_id', None)
        document = await self._get_from_cache(_id) if _id else None
        return document if document else await super().find(**kwargs)

    async def insert(self, data, status=SENT_STATUS_MESSAGE):
        data = generate_message(data, SENT_STATUS_MESSAGE)
        _data = dumps(data)
        await self._set_in_cache(_data, data['_id'])
        await self._send_broker_message(_data)
        return data

    async def update(self, data, query, **kwargs):
        kwargs['upsert'] = True
        await super().update(data, query, **kwargs)

    async def delete_cache(self, data):
        redis_key = _template_key.format(_id=data['_id'])
        await app.redis.execute('del', redis_key)

    async def _set_in_cache(self, data, _id):
        redis_key = _template_key.format(_id=_id)
        await app.redis.execute('set', redis_key, data)

    async def _get_from_cache(self, _id):
        redis_key = _template_key.format(_id=_id)
        message = await app.redis.execute('get', redis_key)
        return loads(message.decode()) if message else message

    async def _send_broker_message(self, body):
        message = aio_pika.Message(body=body.encode())
        channel = app.broker.get_channel()
        await channel.default_exchange.publish(message, routing_key=_queue)
