from betbright.models import message as message_model
from tests.fixture import sent_message


def test_collection_name(server):
    assert message_model.collection.name == 'message'


async def test_find_message_in_redis(message):
    expected = await message(sent_message, 'redis')
    result = await message_model.find(_id=expected['_id'])
    assert result['_id'] == expected['_id']
