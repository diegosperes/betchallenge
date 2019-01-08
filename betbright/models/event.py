import pymongo

from betbright.application import app


async def find(page=0, limit=10, sort=None, unique=False, **query):
    page = page - 1 if page >= 1 else page
    cursor = app.mongo['event'].find(query)
    if sort:
        cursor.sort([(sort, pymongo.DESCENDING)])
    cursor = cursor.skip(page * limit).limit(limit)
    result = await cursor.to_list(limit)
    return result[0] if result and unique else result


async def insert(data):
    await app.mongo['event'].insert_one(data)


async def update(data):
    query = {'id': data['id']}
    document = await find(unique=True, **query)
    document.update(data)
    del document['_id']
    await app.mongo['event'].update_one(query, {'$set': document})
