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
    _id = ObjectId()
    redis_key = 'message_{_id}'.format(_id=_id)

    # setup
    async def factory(fixture, database):
        data = fixture.copy()
        data['_id'] = _id
        if database == 'mongo':
            await server.app.mongo['message'].insert_one(data)
        elif database == 'redis':
            await server.app.redis.execute('set', redis_key, dumps(data))
        else:
            return
        return data
    yield factory

    # teardown
    await server.app.redis.execute('del', redis_key)
    await server.app.mongo['message'].delete_one({'_id': _id})
