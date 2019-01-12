from betbright.models import event


def test_collection_name(server):
    assert event.collection.name == 'event'
