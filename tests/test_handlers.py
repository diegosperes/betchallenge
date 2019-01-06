from bson.objectid import ObjectId
from bson.json_util import loads

from tests.fixture import (
    not_exist_message, scheduled_message, processed_message
)


async def get_json(template, server, expected):
    uri = template.format(**expected)
    response = await server.get(uri)
    return response, loads(await response.text())


async def test_get_scheduled_message(server, message):
    expected = await message(scheduled_message, 'redis')
    response, data = await get_json('/message/{_id}', server, expected)
    assert response.status == 200
    assert expected['_id'] == data['_id']
    assert expected['status'] == data['status']


async def test_get_processed_message(server, message):
    expected = await message(processed_message, 'mongo')
    response, data = await get_json('/message/{_id}', server, expected)
    assert response.status == 200
    assert expected['_id'] == data['_id']
    assert expected['status'] == data['status']


async def test_get_message_when_does_not_exist(server):
    expected = {'_id': ObjectId()}
    response, data = await get_json('/message/{_id}', server, expected)
    assert response.status == 404
    assert not_exist_message == await response.json()
