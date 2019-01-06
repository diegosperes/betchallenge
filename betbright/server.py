from sanic.response import json
from bson.objectid import ObjectId
from bson.json_util import dumps, loads

from betbright.application import app


async def _get_message(_id):
    redis_key = 'message_{_id}'.format(_id=_id)
    message = await app.redis.execute('get', redis_key)
    if not message:
        query = {'_id': ObjectId(_id)}
        message = await app.mongo['message'].find_one(query)
    else:
        message = loads(message.decode())
    return message


@app.route('/message/<_id>')
async def get_message(request, _id):
    message = await _get_message(_id)
    data, status = (message, 200) if message else ({}, 404)
    return json(data, status=status, dumps=dumps)


if __name__ == '__main__':
    app.run()
