import pymongo
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


async def _get_event(value, page=0, limit=10, sort=None):
    result = None
    page = page - 1 if page >= 1 else page
    if value.isnumeric():
        query = {'id': int(value)}
        result = await app.mongo['event'].find_one(query)
    else:
        query = {'sport.name': value}
        cursor = app.mongo['event'].find(query)
        cursor = cursor.skip(page * limit).limit(limit)
        if sort:
            cursor.sort([(sort, pymongo.DESCENDING)])
        result = await cursor.to_list(limit)
        print('result', result)
    return result


@app.route('/message/<_id>', methods=['GET'])
async def get_message(request, _id):
    message = await _get_message(_id)
    data, status = (message, 200) if message else ({}, 404)
    return json(data, status=status, dumps=dumps)


@app.route('/api/match/<value>', methods=['GET'])
async def get_event(request, value):
    kwargs = {
        'page': int(request.raw_args.get('page', '0')),
        'sort': request.raw_args.get('ordering', None)
    }
    event = await _get_event(value, **kwargs)
    data, status = (event, 200) if event else ({}, 404)
    return json(data, status=status, dumps=dumps)


if __name__ == '__main__':
    app.run()
