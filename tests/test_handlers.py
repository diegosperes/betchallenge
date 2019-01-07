import pytest
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

from tests.fixture import (
    sent_message, scheduled_message, processed_message,
    event as _event, message as _message
)


async def get_json(template, server, expected):
    uri = template.format(**expected)
    response = await server.get(uri)
    return response, loads(await response.text())


@pytest.mark.skip('Doing mvp')
async def test_get_sent_message(server, message):
    expected = await message(sent_message, 'redis')
    response, data = await get_json('/message/{_id}', server, expected)
    assert response.status == 200
    assert expected['_id'] == data['_id']
    assert expected['status'] == data['status']


@pytest.mark.skip('Doing mvp')
async def test_get_scheduled_message(server, message):
    expected = await message(scheduled_message, 'mongo')
    response, data = await get_json('/message/{_id}', server, expected)
    assert response.status == 200
    assert expected['_id'] == data['_id']
    assert expected['status'] == data['status']


@pytest.mark.skip('Doing mvp')
async def test_get_processed_message(server, message):
    expected = await message(processed_message, 'mongo')
    response, data = await get_json('/message/{_id}', server, expected)
    assert response.status == 200
    assert expected['_id'] == data['_id']
    assert expected['status'] == data['status']


@pytest.mark.skip('Doing mvp')
async def test_get_message_when_does_not_exist(server):
    kwargs = {'_id': ObjectId()}
    response, data = await get_json('/message/{_id}', server, kwargs)
    assert response.status == 404
    assert {} == await response.json()


async def test_post_message(server):
    response = await server.post('/message/', data=dumps(_message))
    data = await response.json()
    await server.app.mongo['event'].delete_one({'id': data['id']})
    assert response.status == 201
    assert _event['id'] == data['id']
    assert _event['name'] == data['name']


async def test_post_message_when_already_exist(server, event):
    evt = await event(_event)
    evt['name'] = 'New game'
    new_message = _message.copy()
    new_message['event'] = evt
    new_message['message_type'] = 'UpdateOdds'
    response = await server.post('/message/', data=dumps(new_message))
    data = await response.json()
    await server.app.mongo['event'].delete_one({'id': data['id']})
    assert response.status == 200
    assert _event['id'] == data['id']
    assert data['name'] == 'New game'


async def test_get_event_by_id(server, event):
    expected = await event(_event)
    response, data = await get_json('/api/match/{id}', server, expected)
    assert response.status == 200
    assert expected['_id'] == data['_id']


async def test_get_event_by_id_when_does_not_exist(server):
    kwargs = {'id': 123456}
    response, data = await get_json('/api/match/{id}', server, kwargs)
    assert response.status == 404
    assert {} == data


async def test_get_event_by_sport(server, event):
    expected = await event(_event)
    url = '/api/match/{sport[name]}'
    response, data = await get_json(url, server, expected)
    assert response.status == 200
    assert len(data) == 1
    assert expected['_id'] == data[0]['_id']


async def test_get_event_by_sport_and_sort_it(server, event):
    expected = [await event(_event) for i in range(2)]
    url = '/api/match/{sport[name]}?ordering=_id'
    response, data = await get_json(url, server, expected[0])
    assert response.status == 200
    assert len(data) == 2
    assert expected[1]['_id'] == data[0]['_id']
    assert expected[0]['_id'] == data[1]['_id']


async def test_get_event_by_sport_paginate_and_sort_it(server, event):
    expected = [await event(_event) for i in range(11)]
    url = '/api/match/{sport[name]}?page=2&ordering=_id'
    response, data = await get_json(url, server, expected[0])
    assert response.status == 200
    assert len(data) == 1
    assert expected[0]['_id'] == data[0]['_id']


async def test_get_event_by_sport_when_does_not_exist(server):
    url = '/api/match/{sport[name]}'
    response, data = await get_json(url, server, _event)
    assert response.status == 404
    assert {} == data


async def test_get_event_by_sport_and_sort_it_when_does_not_exist(server):
    url = '/api/match/{sport[name]}?ordering=_id'
    response, data = await get_json(url, server, _event)
    assert response.status == 404
    assert {} == data


async def test_get_event_by_sport_and_paginate_it_when_does_not_exist(server):
    url = '/api/match/{sport[name]}?page=2'
    response, data = await get_json(url, server, _event)
    assert response.status == 404
    assert {} == data


async def test_get_event_by_attr(server, event):
    [await event(_event) for i in range(2)]
    url = '/api/match/?name=Real+Madrid+vs+Barcelona'
    response, data = await get_json(url, server, {})
    assert response.status == 200
    assert len(data) == 2


async def test_get_event_by_attr_and_sort_it(server, event):
    expected = [await event(_event) for i in range(2)]
    url = '/api/match/?name=Real+Madrid+vs+Barcelona&ordering=_id'
    response, data = await get_json(url, server, {})
    assert response.status == 200
    assert len(data) == 2
    assert expected[1]['_id'] == data[0]['_id']
    assert expected[0]['_id'] == data[1]['_id']


async def test_get_event_by_attr_paginate_and_sort_it(server, event):
    expected = [await event(_event) for i in range(11)]
    url = '/api/match/?name=Real+Madrid+vs+Barcelona&ordering=_id&page=2'
    response, data = await get_json(url, server, {})
    assert response.status == 200
    assert len(data) == 1
    assert expected[0]['_id'] == data[0]['_id']


async def test_get_event_by_attr_when_does_not_exist(server):
    url = '/api/match/?name=Real+Madrid+vs+Barcelona'
    response, data = await get_json(url, server, _event)
    assert response.status == 404
    assert {} == data


async def test_get_event_by_attr_and_sort_it_when_does_not_exist(server):
    url = '/api/match/?name=Real+Madrid+vs+Barcelona&ordering=_id'
    response, data = await get_json(url, server, _event)
    assert response.status == 404
    assert {} == data


async def test_get_event_by_attr_and_paginate_it_when_does_not_exist(server):
    url = '/api/match/?name=Real+Madrid+vs+Barcelona&page=2'
    response, data = await get_json(url, server, _event)
    assert response.status == 404
    assert {} == data
