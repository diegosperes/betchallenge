from bson.json_util import loads

from betbright.application import app
from betbright.models.model import Model


class Message(Model):
    @property
    def collection(self):
        return app.mongo['message']

    async def find(self, **kwargs):
        _id = kwargs.get('_id', None)
        document = await self._find_in_redis(_id) if _id else None
        return document if document else await super().find(**kwargs)

    async def _find_in_redis(_id):
        redis_key = 'message_{_id}'.format(_id=_id)
        message = await app.redis.execute('get', redis_key)
        return loads(message.decode()) if message else message
