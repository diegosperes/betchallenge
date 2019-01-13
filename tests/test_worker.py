from datetime import datetime
from bson.objectid import ObjectId

from betbright.models import message
from tests.fixture import message as _message


async def test_consume_data_from_broker(server, worker):
    data = await message.insert(_message.copy())
    await worker.execute()
    document = await message.find(_id=data['_id'], unique=True)

    assert document['status'] == 'processed'
    assert document['@uri'] == '/api/match/{event[id]}'.format(**document)
    assert type(document['scheduled_at']) == datetime
    assert type(document['processed_at']) == datetime
    assert type(document['sent_at']) == datetime
    assert type(document['_id']) == ObjectId
    assert document['event'] is not None
