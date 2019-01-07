import pymongo

from betbright.application import app


async def find(value, page=0, limit=10, sort=None, **query):
    if query:
        return await _get_event_by_attr(query, page, limit, sort)
    elif type(value) is int or value.isnumeric():
        return await _get_event_by_id(value)
    return await _get_event_by_attr({'sport.name': value}, page, limit, sort)


async def insert(data):
    await app.mongo['event'].insert_one(data)


async def update(data):
    query = {'id': data['id']}
    document = await find(data['id'])
    document.update(data)
    del document['_id']
    await app.mongo['event'].update_one(query, {'$set': document})


async def _get_event_by_id(_id):
    query = {'id': int(_id)}
    return await app.mongo['event'].find_one(query)


async def _get_event_by_attr(query, page, limit, sort):
    page = page - 1 if page >= 1 else page
    cursor = app.mongo['event'].find(query)
    if sort:
        cursor.sort([(sort, pymongo.DESCENDING)])
    cursor = cursor.skip(page * limit).limit(limit)
    return await cursor.to_list(limit)
