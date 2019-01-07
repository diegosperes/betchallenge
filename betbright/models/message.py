import aio_pika
from datetime import datetime
from bson.json_util import loads, dumps
from bson.objectid import ObjectId

from betbright.application import app


async def find(_id):
    document = await _get_by_id_from_redis(_id)
    if not document:
        return await _get_by_id_from_mongo(_id)
    return document


async def publish(message):
    message['_id'] = ObjectId()
    channel = await app.pika.channel()
    redis_key = 'message_{_id}'.format(**message)
    body = dumps(message).encode()
    await channel.default_exchange.publish(
        aio_pika.Message(body=body), routing_key='message')
    await app.redis.execute('set', redis_key, dumps(_get_template()))
    return message


async def _get_by_id_from_redis(_id):
    redis_key = 'message_{_id}'.format(_id=_id)
    message = await app.redis.execute('get', redis_key)
    return loads(message.decode()) if message else message


async def _get_by_id_from_mongo(_id):
    query = {'_id': ObjectId(_id)}
    return await app.mongo['message'].find_one(query)


def _get_template():
    return {
       "@uri": None,
       "status": "sent",
       "send_at": datetime.now(),
       "scheduled_at": None,
       "processed_at": None,
    }
