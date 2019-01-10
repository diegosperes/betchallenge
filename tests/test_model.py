

async def test_insert_data(test_model):
    data = {'name': 'diego'}
    await test_model.insert(data)
    document = await test_model.collection.find_one(data)
    assert data == document


async def test_update_document(test_model):
    data = {'name': 'diego'}
    await test_model.collection.insert_one(data)
    data['name'] = 'pedro'
    await test_model.update(data, {'_id': data['_id']})
    document = await test_model.collection.find_one({'name': data['name']})
    assert document is not None


async def test_find_document_by_id(test_model):
    data = {'name': 'diego'}
    await test_model.collection.insert_one(data)
    document = await test_model.find(**{'_id': data['_id'], 'unique': True})
    assert data == document


async def test_find_documents_by_attr(test_model):
    data = {'name': 'diego'}
    await test_model.collection.insert_one(data)
    documents = await test_model.find(**{'name': data['name']})
    assert [data] == documents


async def test_find_and_paginate_zero_page(test_model):
    insert = test_model.collection.insert_one
    [await insert({'name': 'diego', '_id': id}) for id in range(11)]
    documents = await test_model.find(**{'name': 'diego', 'page': 0})
    assert len(documents) == 10


async def test_find_and_paginate_first_page(test_model):
    insert = test_model.collection.insert_one
    [await insert({'name': 'diego', '_id': id}) for id in range(11)]
    documents = await test_model.find(**{'name': 'diego', 'page': 1})
    assert len(documents) == 10


async def test_find_and_paginate_second_page(test_model):
    insert = test_model.collection.insert_one
    [await insert({'name': 'diego', '_id': id}) for id in range(11)]
    documents = await test_model.find(**{'name': 'diego', 'page': 2})
    assert len(documents) == 1


async def test_find_and_increase_limit(test_model):
    insert = test_model.collection.insert_one
    [await insert({'name': 'diego', '_id': id}) for id in range(20)]
    documents = await test_model.find(**{'name': 'diego', 'limit': 15})
    assert len(documents) == 15


async def test_find_and_sort_by_field(test_model):
    insert = test_model.collection.insert_one
    [await insert({'name': 'diego', '_id': id}) for id in range(20)]
    documents = await test_model.find(**{'name': 'diego', 'sort': '_id'})
    assert documents[0]['_id'] == 19
    assert documents[9]['_id'] == 10
