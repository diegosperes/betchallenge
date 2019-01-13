import aioredis
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic

from betbright.config import settings
from betbright.broker import Broker


class Application(Sanic):
    def run(self, *args, **kwargs):
        settings['app'].update(kwargs)
        super().run(*args, **settings['app'])


app = Application()


def settings_update(app, loop):
    app.config.update(settings)


def mongodb_setup(app, loop):
    uri = app.config.mongo['uri']
    database = app.config.mongo['database']
    app.mongo = AsyncIOMotorClient(uri, io_loop=loop)[database]


async def redis_setup(app, loop):
    uri = app.config.redis['uri']
    app.redis = await aioredis.create_pool(uri, minsize=5, loop=loop)


async def broker_setup(app, loop):
    app.broker = await Broker(loop).connect()


async def redis_teardown(app, loop):
    app.redis.close()
    await app.redis.wait_closed()


async def broker_teardown(app, loop):
    await app.broker.disconnect()


@app.listener('before_server_start')
async def setup(app, loop):
    settings_update(app, loop)
    mongodb_setup(app, loop)
    await redis_setup(app, loop)
    await broker_setup(app, loop)


@app.listener('before_server_stop')
async def teardown(app, loop):
    await redis_teardown(app, loop)
    await broker_teardown(app, loop)
