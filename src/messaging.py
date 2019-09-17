from azure.eventhub.aio import EventHubClient
from azure.eventhub.aio.eventprocessor import (
    EventProcessor,
    PartitionProcessor,
    SamplePartitionManager,
)
from azure.eventhub.extensions.checkpointstoreblobaio import BlobPartitionManager
from azure.storage.blob.aio import ContainerClient
import logging
import json
import asyncio
import queue
import datetime


class Async_EventHub_Connector:
    def __init__(self, eh_connection_string, sa_connection_string, sa_container_name):
        import app

        self._eh_connection_string = eh_connection_string
        self._sa_connection_string = sa_connection_string
        self._sa_container_name = sa_container_name
        self._queue = app.message_queue

    def __enter__(self):
        # self._event_loop = asyncio.get_event_loop()
        self._client = EventHubClient.from_connection_string(self._eh_connection_string)
        # TODO replace with persistion
        self._storage_client = ContainerClient.from_connection_string(
            conn_str=self._sa_connection_string, container=self._sa_container_name
        )
        self._partition_manager = BlobPartitionManager(self._storage_client)
        self._event_processor = EventProcessor(
            self._client, "$default", MyPartitionProcessor, self._partition_manager
        )

    async def aexit(self):
        await self._event_processor.stop()
        # await self._partition_manager.close()
        await self._client.close()

    def __exit__(self, type, value, traceback):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.aexit())
        loop.close()

    async def _receiver_loop(self):
        # write messages to event hub
        async with self._storage_client:
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
    async def initialize(self, partition_context):
        import app

        self._queue = app.message_queue

    async def process_events(self, events, partition_context):
        if events:
            await asyncio.gather(*[self._process_event(event) for event in events])
            await partition_context.update_checkpoint(
                events[-1].offset, events[-1].sequence_number
            )

    async def _process_event(self, event):
        print(f"Getting: {event.sequence_number} enqueued at {event.enqueued_time}")
        self._queue.put(event.body_as_json())
