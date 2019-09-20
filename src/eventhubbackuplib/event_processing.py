from .db_controller import DB_Controller
from .plugins.plugin_loader import Plugin_Loader
from azure.eventhub import EventData
import threading
import logging
import queue 

logger = logging.getLogger(__name__)


class Event_Processing:
    """Connects to PostgreSQL database to insert messages from queue

    First connects to TimescaleDB to insert messages from the queue.
    This happens in multiple threads.

    Attributes:
        number_of_threads: Number of threads with which the partition processor
            using this class should work on the events.
    """

    def __init__(
        self,
        connection_string: str,
        table_name: str,
        plugin_name: str,
        number_of_threads: int,
    ):
        """Init the DB_connector class

        Uses global EventHubBackup.message_queue as queue.

        Args:
            connection_string: connection_string for database in format:
                "dbname=... user=... password=... host=... port=..."
            table_name: name of the db table to write the data to
            plugin_name: name of the parser_plugin to process the data with
                (filename and classname have to be the same by default)
            number_of_threads: Number of threads with which the partition processor
                using this class should work on the events.

        """

        # import EventHubBackup to get global message_queue, not possible on top because of circular import

        self._connection_string = connection_string
        self._table_name = table_name
        self._plugin_name = plugin_name
        self.number_of_threads = number_of_threads

        logger.debug(f"{self.__hash__()}: Created processing client")

    def __enter__(self):
        self.db_controller = DB_Controller(self._connection_string)
        self._plugin = Plugin_Loader.load(class_name=self._plugin_name)

    def __exit__(self, type, value, traceback):
        self.db_controller.close()

    def process_message(self, message: str) -> None:
        "Process a message with the set plugin"
        data = self._plugin.process(message)
        self.db_controller.insert(self._table_name, [data])

    def process_event(self, event: EventData, error_queue: queue.Queue) -> None:
        """Process an event from event hub

        Uses process_message to process the event body.
        If an error occors it will be put into the queue.

        Args:
            event: Event to be processed.
            error_queue: queue for occuring errors to be handled by calling process
        """
        logger.debug(
            f"{self.__hash__()}: Processing event with sn {event.sequence_number} and offset {event.offset}"
        )
        try:
            self.process_message(event.body_as_str())
            
        except Exception as e:
            error_queue.put([event, e])
