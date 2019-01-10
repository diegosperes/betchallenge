import pymongo


def cursor_setup(cursor, page, limit, sort):
    '''Paginate and sort a mongo cursor'''
    if sort:
        cursor.sort([(sort, pymongo.DESCENDING)])
    cursor.skip(page * limit).limit(limit)


class Model:
    @property
    def collection(self):
        raise NotImplementedError()

    async def find(self, page=0, limit=10, sort=None, unique=False, **query):
        page = page - 1 if page >= 1 else page
        cursor = self.collection.find(query)
        cursor_setup(cursor, page, limit, sort)
        result = await cursor.to_list(limit)
        return result[0] if result and unique else result

    async def insert(self, data):
        await self.collection.insert_one(data)

    async def update(self, data, query):
        data = data.copy()
        document = await self.find(unique=True, **query)
        document.update(data)
        del document['_id']
        await self.collection.update_one(query, {'$set': document})
