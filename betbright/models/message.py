from bson.objectid import ObjectId
from bson.json_util import loads, dumps

from betbright.application import app
from betbright.models.model import Model


SENT_STATUS_MESSAGE = 'sent'
SCHEDULED_STATUS_MESSAGE = 'scheduled'
PROCESSED_STATUS_MESSAGE = 'processed'

_template_key = 'message_{_id}'


class Message(Model):
    @property
    def collection(self):
        return app.mongo['message']

    async def find(self, **kwargs):
        _id = kwargs.get('_id', None)
        document = await self._find_in_redis(_id) if _id else None
        return document if document else await super().find(**kwargs)

    async def insert(self, data):
        data['_id'] = ObjectId()
        redis_key = _template_key.format(_id=data['_id'])
        await app.redis.execute('set', redis_key, dumps(data))

    async def update(self, data, query, **kwargs):
        kwargs['upsert'] = True
        await super().update(data, query, **kwargs)

    async def _find_in_redis(self, _id):
        redis_key = _template_key.format(_id=_id)
        message = await app.redis.execute('get', redis_key)
        return loads(message.decode()) if message else message
