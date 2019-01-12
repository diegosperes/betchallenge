from betbright.models import message as message_model
from tests.fixture import sent_message, scheduled_message, processed_message


def test_collection_name(server):
    assert message_model.collection.name == 'message'


async def test_find_message_in_redis(message):
    expected = await message(sent_message, 'redis')
    result = await message_model.find(_id=expected['_id'])
    assert result['_id'] == expected['_id']


async def test_insert_sent_message_in_redis(server):
    redis = server.app.redis
    raw_message = sent_message.copy()
    await message_model.insert(raw_message)
    result = await redis.execute('get', 'message_{_id}'.format(**raw_message))
    assert result is not None


async def test_update_scheduled_message_in_mongo(message):
    expected = await message(sent_message, 'redis')
    query = {'_id': expected['_id']}
    expected.update(scheduled_message)
    await message_model.update(expected, query)
    assert await message_model.collection.find_one(query) is not None


async def test_update_processed_message_in_mongo(message):
    expected = await message(scheduled_message, 'mongo')
    query = {'_id': expected['_id']}
    expected.update(processed_message)
    await message_model.update(expected, query)
    assert await message_model.collection.find_one(query) is not None
