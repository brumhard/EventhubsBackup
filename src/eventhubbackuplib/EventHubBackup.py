from .event_processing import Event_Processing
from .messaging import EventHub_Receiver
import queue
import logging
from contextlib import ExitStack
from .partition_processor import PartitionProcessorWrapper

message_queue = queue.Queue()

logger = logging.getLogger(__name__)


class EventHubBackup:
    """Main class to run the backup tool

    Connects to an eventhub and receives the events.
    Checkpoints (for keeping track on which events are processed)
    are saved to an azure blob storage container.
    Event data will be processed with parser plugin and written to
    a postgres db.
    """

    def __init__(
        self,
        db_worker_threads: int,
        db_connection_string: str,
        db_table_name: str,
        plugin_name: str,
        eh_connection_string: str,
        sa_connection_string: str,
        sa_container_name: str,
    ):
        """Init EventHubBackup class:
        
        Args:
            db_worker_threads: Number of threads that should be used for each partition
                processor when processing the event batches
            db_connection_string: connection string for the postgresDB (timescaleDB)
                format: 'dbname=<name of db> user=<db user> password=<password for db user> host=<host of db> port=<db port>'
            db_table_name: name of the db's table where the data should be stored,
            plugin_name: name of the parser plugin to be used to transform the data
                to the needed format for the table
            eh_connection_string: connection string for the event hub from which to pull the data
                format: 'Endpoint=...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...'
            sa_connection_string: connection string for azure storage account
                format: see https://docs.microsoft.com/en-us/azure/storage/common/storage-account-manage#view-account-keys-and-connection-string
            sa_container_name: name of the container to store the checkpoint data.
                It's mandatory to have one container for each event hub
        """
        self._db_worker_threads = db_worker_threads
        self._db_connection_string = db_connection_string
        self._db_table_name = db_table_name
        self._plugin_name = plugin_name
        self._eh_connection_string = eh_connection_string
        self._sa_connection_string = sa_connection_string
        self._sa_container_name = sa_container_name

    def start(self) -> None:
        "Start the backup loop (in main thread)"

        logger.info("Started backup")
        with ExitStack() as stack:
            logger.info(
                f"Starting event processing in {self._db_worker_threads} threads"
            )
            processor = Event_Processing(
                self._db_connection_string,
                self._db_table_name,
                self._plugin_name,
                self._db_worker_threads,
            )
            stack.enter_context(processor)

            wrapper = PartitionProcessorWrapper()
            wrapper.set_event_processing(processor)

            receiver = EventHub_Receiver(
                self._eh_connection_string,
                self._sa_connection_string,
                self._sa_container_name,
                wrapper.get_partition_processor(),
            )
            with receiver:
                receiver.receive_messages()

