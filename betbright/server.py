from sanic.response import json
from bson.json_util import dumps

from betbright.application import app
from betbright.models import message, event


@app.route('/message/<_id>', methods=['GET'])
async def get_message(request, _id):
    document = await message.find(_id)
    data, status = (document, 200) if document else ({}, 404)
    return json(data, status=status, dumps=dumps)


@app.route('/api/match/<value>', methods=['GET'])
async def get_event(request, value):
    kwargs = {
        'page': int(request.raw_args.get('page', '0')),
        'sort': request.raw_args.get('ordering', None)
    }
    document = await event.find(value, **kwargs)
    data, status = (document, 200) if document else ({}, 404)
    return json(data, status=status, dumps=dumps)


if __name__ == '__main__':
    app.run()
