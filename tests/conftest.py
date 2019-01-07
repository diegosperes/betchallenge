import pytest
from bson.objectid import ObjectId
from bson.json_util import dumps

from betbright.server import app


@pytest.fixture(scope='function')
def server(loop, test_client):
    client = test_client(app)
    return loop.run_until_complete(client)


@pytest.fixture(scope='function')
async def message(server):
    ids = []
    template_key = 'message_{_id}'

    # setup
    async def factory(fixture, database):
        data = fixture.copy()
        data['_id'] = ObjectId()
        if database == 'mongo':
            await server.app.mongo['message'].insert_one(data)
        elif database == 'redis':
            redis_key = template_key.format(_id=data['_id'])
            await server.app.redis.execute('set', redis_key, dumps(data))
        else:
            return
        ids.append(data['_id'])
        return data
    yield factory

    # teardown
    for _id in ids:
        await server.app.redis.execute('del', template_key.format(_id=_id))
        await server.app.mongo['message'].delete_one({'_id': _id})


@pytest.fixture(scope='function')
async def event(server):
    ids = []

    # setup
    async def factory(fixture):
        data = fixture.copy()
        data['_id'] = ObjectId()
        await server.app.mongo['event'].insert_one(data)
        ids.append(data['_id'])
        return data
    yield factory

    # teardown
    for _id in ids:
        await server.app.mongo['event'].delete_one({'_id': _id})


@pytest.fixture(scope='function')
async def broker(server):
    queue_names = {'message'}
    channel = await server.app.pika.channel()

    # setup
    async def get_queue(queue_name):
        queue_names.add(queue_name)
        return await channel.declare_queue(queue_name, passive=True)
    yield get_queue

    # teardown
    for queue_name in queue_names:
        await channel.queue_delete(queue_name)
    await channel.close()
