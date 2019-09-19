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

logger = logging.getLogger(__name__)


class EventHub_Receiver:
    """ Connects to Azure Event Hub to receive messages.

    Uses the EventProcessor from Azure SDK to connect to Event Hub 
    and receive the needed messages.
    Checkpoints are stored in Azure Blob Storage to keep track of
    which messages have been processed already.
    """

    def __init__(
        self,
        eh_connection_string: str,
        sa_connection_string: str,
        sa_container_name: str,
        partition_processor,
    ):
        """Init the Async_EventHub_Connector class

        Args:
            eh_connection_string: connection string for event hub in format:
                `"Endpoint=...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=..."`
            sa_connection_string: connection string for storage blob storage
                https://docs.microsoft.com/en-us/azure/storage/common/storage-account-manage#view-account-keys-and-connection-string
            sa_container_name: name of container in blob storage to be used for checkpoints               
        """

        self._eh_connection_string = eh_connection_string
        self._sa_connection_string = sa_connection_string
        self._sa_container_name = sa_container_name
        self._partition_processor = partition_processor

        logger.debug(f"{self.__hash__()}: Created EventHub_Receiver")

    def __enter__(self):
        self._client = EventHubClient.from_connection_string(self._eh_connection_string)
        self._storage_client = ContainerClient.from_connection_string(
            conn_str=self._sa_connection_string, container=self._sa_container_name
        )
        self._partition_manager = BlobPartitionManager(self._storage_client)
        self._event_processor = EventProcessor(
            self._client, "$default", self._partition_processor, self._partition_manager
        )

    async def aexit(self):
        await self._event_processor.stop()
        # await self._partition_manager.close()
        await self._client.close()

    def __exit__(self, type, value, traceback):
        # convert async exits to sync
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.aexit())
        loop.close()

    async def _receiver_loop(self) -> None:
        # write messages to event hub, start is active as long as it runs
        async with self._storage_client:
            await self._event_processor.start()

    def receive_messages(self) -> None:
        """Start listening to event hub

        Starts the Event Processor to get messages from event hub
        and process them using MyPartitionProcessor.
        """
        logger.info("Starting async receiving messages")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._receiver_loop())

