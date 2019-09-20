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

    Should only be used with PartitionProcessorWrapper to init global vars.
    Used by EventProcessor to handle the events.
    Used for load balancing (new instance created when needed)
    Uses the global var event_processing to init the property as
    now input parameters can be set in event processor.
    """

    async def initialize(self, partition_context):
        """Init function used by event processor instead of __init__()
        
        If the global var event_processing isn't set it will raise an error
        as this is required. Can be set with wrapper class below.
        """
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

        Processes all events asynchronously in multiple threads set 
        by number of threads in event_processing.
        All errors from the threads are handled afterwards.
        If error occurs all changes will be rolled back and exit.
        If no error occurs the changes are commited.
        """
        if events:
            logger.info(f"{self.__hash__()}: Start processing {len(events)} events from sn {events[0].sequence_number}")

            # asynchonously process events in multiple threads
            # any occuring errors are put into queue
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
                    # only first event of queue is important as others will fail because of this
                    event, err = error_queue.get()
                    logger.error(f"{self.__hash__()}: Error occured in event with sn {event.sequence_number}: {err}")
                # rollback all changes made when processing events
                self._event_processing.db_controller.rollback()
                raise Exception(f"{self.__hash__()}: 1 or more critical errors in processing")
            else:
                # only commit if no errors happened
                self._event_processing.db_controller.commit()
                # update checkpoint in storage account
                await partition_context.update_checkpoint(
                    events[-1].offset, events[-1].sequence_number
                )

    async def process_error(self, error, partition_context: PartitionContext):
        sys.exit(f"Critical Error in Partition Processor: {error}")



class PartitionProcessorWrapper:
    """class used to initilialize the partition processor

    As the partition_processor cannot receive arguments 
    it uses globals that can be initialized with this class
    """
    def __init__(self):
        self._processor_type = None

    def set_event_processing(self, event_processing_unit: Event_Processing):
        """Set required global var for the partition processor"""
        global event_processing
        event_processing = event_processing_unit
        self._processor_type = MyPartitionProcessor

    def get_partition_processor(self):
        """Return the partition processor
        
        Only to be used after initilized with set_event_processing,
        otherwise error will occur.
        """
        if(self._processor_type == None):
            raise Exception("Call set_event_processing() first to init required globals.")
        return self._processor_type

