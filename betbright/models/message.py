from bson.json_util import loads
from bson.objectid import ObjectId

from betbright.application import app


async def find(_id):
    document = await _get_by_id_from_redis(_id)
    if not document:
        return await _get_by_id_from_mongo(_id)
    return document


async def _get_by_id_from_redis(_id):
    redis_key = 'message_{_id}'.format(_id=_id)
    message = await app.redis.execute('get', redis_key)
    return loads(message.decode()) if message else message


async def _get_by_id_from_mongo(_id):
    query = {'_id': ObjectId(_id)}
    return await app.mongo['message'].find_one(query)
