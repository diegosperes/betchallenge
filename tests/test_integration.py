from bson.json_util import dumps, loads

from betbright.models import event
from tests.fixture import message as _message


async def test_must_not_override_event_with_message_metadata(server, worker):
    await worker.execute()
    response = await server.post('/message/', data=dumps(_message))
    data = loads(await response.text())
    await worker.execute()

    _message2 = _message.copy()
    _message2['message_type'] = 'UpdateOdds'
    await server.post('/message/', data=dumps(_message2))
    await worker.execute()

    document = await event.find(id=data['event']['id'], unique=True)
    assert '@uri' not in document
    assert 'event' not in document
    assert 'status' not in document
    assert 'sent_at' not in document
    assert 'scheduled_at' not in document
    assert 'processed_at' not in document
