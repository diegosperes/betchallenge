from sanic.response import json
from bson.json_util import dumps

from betbright.application import app
from betbright.models import message, event


async def _get_event(request, value=None):
    querystring = request.raw_args.copy()
    querystring['page'] = int(request.raw_args.get('page', '0'))
    querystring['sort'] = request.raw_args.get('ordering', None)
    if 'ordering' in querystring:
        del querystring['ordering']

    document = await event.find(value, **querystring)
    data, status = (document, 200) if document else ({}, 404)
    return json(data, status=status, dumps=dumps)


@app.route('/message/<_id>', methods=['GET'])
async def get_message(request, _id):
    document = await message.find(_id)
    data, status = (document, 200) if document else ({}, 404)
    return json(data, status=status, dumps=dumps)


@app.route('/message/', methods=['POST'])
async def post_message(request):
    _message = await message.publish(request.json)
    location = '{scheme}://{host}/message/{id}'.format(
        scheme=request.scheme, host=request.host, id=_message['_id'])
    return json({}, status=202, headers={'Location': location})


@app.route('/api/match/<value>', methods=['GET'])
async def get_event(request, value):
    return await _get_event(request, value)


@app.route('/api/match/', methods=['GET'])
async def get_event_by_attr(request):
    return await _get_event(request)


if __name__ == '__main__':
    app.run()
