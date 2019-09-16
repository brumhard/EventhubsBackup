from azure.eventhub.aio import EventHubClient
from azure.eventhub import EventData, EventPosition
import logging
import json
import asyncio


class Async_EventHub_Connector:
    def __init__(self, connection_string):
        self._client = EventHubClient.from_connection_string(connection_string)
        self._close = False

    def __enter__(self):
        self._event_loop = asyncio.get_event_loop()
        self._consumer = self._client.create_consumer(
            consumer_group="$default",
            partition_id="0",
            event_position=EventPosition("-1"),
        )

    async def aexit(self):
        await self._consumer.close()
        self._client.close()

    def __exit__(self, type, value, traceback):
        self._close = True
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.aexit())
        loop.close()

    async def _receiver_loop(self, queue):
        # write messages to event hub
        while True and not self._close:
            received = await self._consumer.receive(max_batch_size=100, timeout=5)
            for message in received:
                queue.put(message)
                logging.info(f"Got message: {json.loads(message.body_as_json)}")

    def receive_messages(self, queue):
        # self._event_loop.create_task(self._messaging_loop(queue))
        self._event_loop.run_until_complete(self._receiver_loop(queue))
