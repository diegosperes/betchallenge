import pytest
from bson.objectid import ObjectId
from bson.json_util import dumps

from betbright.server import app
from betbright.models.model import Model
from betbright.worker import Worker


class TestModel(Model):
    @property
    def collection(self):
        return app.mongo['test-model']


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
    await server.app.broker.get_channel().queue_delete('message')
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
async def test_model(server):
    test_model = TestModel()
    yield test_model
    await test_model.collection.delete_many({})


@pytest.fixture(scope='function')
async def worker(server):
    app = server.app
    worker = Worker(app.loop)
    await worker.setup()
    yield worker
    await worker.broker.get_channel().queue_delete('message')
    await app.mongo.client.drop_database(app.config.mongo['database'])
    await app.redis.execute('flushdb')
