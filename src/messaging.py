from azure.eventhub.aio import EventHubClient
from azure.eventhub.aio.eventprocessor import (
    EventProcessor,
    PartitionProcessor,
    SamplePartitionManager
)
import logging
import json
import asyncio
import queue
import datetime


class Async_EventHub_Connector:
    def __init__(self, connection_string, queue: queue.Queue):
        self._connection_string = connection_string
        self._queue = queue

    def __enter__(self):
        # self._event_loop = asyncio.get_event_loop()
        self._client = EventHubClient.from_connection_string(self._connection_string)
        # TODO replace with persistion
        self._partition_manager = SamplePartitionManager()
        self._event_processor = EventProcessor(
            self._client, "$default", MyPartitionProcessor, self._partition_manager
        )

    async def aexit(self):
        await self._event_processor.stop()
        await self._partition_manager.close()
        await self._client.close()

    def __exit__(self, type, value, traceback):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.aexit())
        loop.close()


    async def _receiver_loop(self):
        # write messages to event hub
        
        await self._event_processor.start()
        # while True and not self._close:
        #     pass
        #     received = await self._consumer.receive(max_batch_size=100, timeout=5)
        #     for message in received:
        #         queue.put(message)
        #         logging.info(f"Got message: {json.loads(message.body_as_json)}")

    def receive_messages(self):
        # self._event_loop.create_task(self._receiver_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._receiver_loop())
        # self._event_loop.run_forever()


class MyPartitionProcessor(PartitionProcessor):
    # def __init__(self, queue):
    #     self._queue = queue
    async def process_events(self, events, partition_context):
        if events:
            await asyncio.gather(*[self._process_event(event) for event in events])
            await partition_context.update_checkpoint(
                events[-1].offset, events[-1].sequence_number
            )
    async def _process_event(self, event):
        now = datetime.datetime.utcnow().isoformat()
        print(f"{now} ::: {event.body_as_json()}")
        # self._queue.put(event)

