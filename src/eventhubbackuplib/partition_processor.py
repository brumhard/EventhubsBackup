import logging
import asyncio
from azure.eventhub.aio.eventprocessor import PartitionProcessor
from .event_processing import Event_Processing
import concurrent.futures

logger = logging.getLogger(__name__)

event_processing = None


class MyPartitionProcessor(PartitionProcessor):
    """Implementation of abstract class PartitionProcessor
    
    Used by EventProcessor to handle the events.
    Used for load balancing (new instance created when needed)
    """

    async def initialize(self, partition_context):
        """Init function used by event processor instead of __init__()"""
        logger.debug(f"{self.__hash__()}: New PartitionProcessor created")

        global event_processing
        if event_processing == None:
            logger.error(
                "Could't init partition processor as working vars are not set. This is the only way to input parameters"
            )
            raise Exception("Pls initialize event_processing first to use this class.")
        from .EventHubBackup import message_queue

        self._event_processing = event_processing

    async def process_events(self, events, partition_context):
        """Process event hub events

        Writes all events to queue defined globally in EventHubBackup.message_queue.
        """
        if events:
            logger.info(f"{self.__hash__()}: Processing {len(events)} events")
            loop = asyncio.get_event_loop()
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
            blocking = [
                loop.run_in_executor(
                    executor,
                    self._event_processing.process_event,
                    event,
                )
                for event in events
            ]
            await asyncio.wait(blocking)
            await partition_context.update_checkpoint(
                events[-1].offset, events[-1].sequence_number
            )

class PartitionProcessorWrapper:
    def __init__(self):
        self._processor_type = MyPartitionProcessor

    def set_event_processing(self, event_processing_unit):
        global event_processing
        event_processing = event_processing_unit

    def get_partition_processor(self):
        return self._processor_type

