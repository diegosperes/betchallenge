import aioredis
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic

from betbright.config import settings


class Application(Sanic):
    def run(self, *args, **kwargs):
        settings['app'].update(kwargs)
        super().run(*args, **settings['app'])


app = Application()


@app.listener('before_server_start')
def settings_update(app, loop):
    app.config.update(settings)


@app.listener('before_server_start')
def mongodb_setup(app, loop):
    uri = app.config.mongo['uri']
    database = app.config.mongo['database']
    app.mongo = AsyncIOMotorClient(uri, io_loop=loop)[database]


@app.listener('before_server_start')
async def redis_setup(app, loop):
    uri = app.config.redis['uri']
    app.redis = await aioredis.create_pool(uri, minsize=5, loop=loop)


@app.listener('before_server_stop')
async def redis_teardown(app, loop):
    app.redis.close()
    await app.redis.wait_closed()
