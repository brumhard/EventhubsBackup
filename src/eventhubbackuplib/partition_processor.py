import logging
import asyncio
from azure.eventhub.aio.eventprocessor import PartitionProcessor, PartitionContext
from .event_processing import Event_Processing
import concurrent.futures
import queue
import sys

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

    async def process_events(self, events, partition_context: PartitionContext):
        """Process event hub events

        Writes all events to queue defined globally in EventHubBackup.message_queue.
        """
        if events:
            logger.info(f"{self.__hash__()}: Start processing {len(events)} events from sn {events[0].sequence_number}")

            error_queue = queue.Queue()
            loop = asyncio.get_event_loop()
            executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=self._event_processing.number_of_threads
            )
            blocking = [
                loop.run_in_executor(
                    executor, self._event_processing.process_event, event, error_queue
                )
                for event in events
            ]
            await asyncio.wait(blocking)

            logger.info(f"{self.__hash__()}: Done processing {len(events)} events from sn {events[0].sequence_number}")
            if not error_queue.empty():
                while not error_queue.empty():
                    # only first event of queue is important as others
                    err = error_queue.get()
                    logger.error(f"{self.__hash__()}: Error occured in thread: {err}")
                self._event_processing.db_controller.rollback()
                raise Exception(f"{self.__hash__()}: 1 or more critical errors in processing")
            else:
                self._event_processing.db_controller.commit()
                # only commit if no errors happened
                await partition_context.update_checkpoint(
                    events[-1].offset, events[-1].sequence_number
                )

    async def process_error(self, error, partition_context: PartitionContext):
        sys.exit(f"Critical Error in Partition Processor: {error}")
        # raise Exception(f"Critical Error: {error}")



class PartitionProcessorWrapper:
    def __init__(self):
        self._processor_type = MyPartitionProcessor

    def set_event_processing(self, event_processing_unit):
        global event_processing
        event_processing = event_processing_unit

    def get_partition_processor(self):
        return self._processor_type

