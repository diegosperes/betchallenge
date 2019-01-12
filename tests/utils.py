from bson.json_util import loads


async def get_json(template, server, expected):
    uri = template.format(**expected)
    response = await server.get(uri)
    return response, loads(await response.text())
