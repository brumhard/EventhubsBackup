from .event_processing import Event_Processing
from .messaging import EventHub_Receiver
import queue
import logging
from contextlib import ExitStack

message_queue = queue.Queue()

logger = logging.getLogger(__name__)


class EventHubBackup:
    def __init__(
        self,
        db_writer_count,
        db_connection_string,
        db_table_name,
        plugin_name,
        eh_connection_string,
        sa_connection_string,
        sa_container_name,
    ):
        self._db_writer_count = db_writer_count
        self._db_connection_string = db_connection_string
        self._db_table_name = db_table_name
        self._plugin_name = plugin_name
        self._eh_connection_string = eh_connection_string
        self._sa_connection_string = sa_connection_string
        self._sa_container_name = sa_container_name

    def start(self):
        # use ExitStack to close all db connections in the end
        logger.info("Started backup")
        with ExitStack() as stack:
            for i in range(0, self._db_writer_count):
                db = Event_Processing(
                    self._db_connection_string, self._db_table_name, self._plugin_name
                )
                stack.enter_context(db)
                db.process_in_thread()

            receiver = EventHub_Receiver(
                self._eh_connection_string,
                self._sa_connection_string,
                self._sa_container_name,
            )
            with receiver:
                receiver.receive_messages()

