import pymongo

from betbright.application import app


async def find(value, page=0, limit=10, sort=None):
    if value.isnumeric():
        return await _get_event_by_id(value)
    else:
        return await _get_event_by_sport(value, page, limit, sort)


async def _get_event_by_id(_id):
    query = {'id': int(_id)}
    return await app.mongo['event'].find_one(query)


async def _get_event_by_sport(sport, page, limit, sort):
    query = {'sport.name': sport}
    page = page - 1 if page >= 1 else page
    cursor = app.mongo['event'].find(query)
    if sort:
        cursor.sort([(sort, pymongo.DESCENDING)])
    cursor = cursor.skip(page * limit).limit(limit)
    return await cursor.to_list(limit)
