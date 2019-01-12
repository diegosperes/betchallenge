import asyncio
import aio_pika
from betbright.broker import Broker


async def consume_message(loop):
    broker = await Broker(loop).connect()
    queue = await broker.get_queue('message')

    async for message in queue:
        with message.process():
            print('aloha', message.body)

    await broker.disconnect()


async def send_message(loop):
    broker = await Broker(loop).connect()
    channel = broker.get_channel()
    message = aio_pika.Message(body='Hello {}'.format('message').encode())
    await channel.default_exchange.publish(message, routing_key='message')
    await broker.disconnect()


async def main(loop):
    await send_message(loop)
    await consume_message(loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()