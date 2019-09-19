from .db_controller import DB_Controller
from .plugins.plugin_loader import Plugin_Loader
import threading

class Event_Processing:
    """Connects to PostgreSQL database to insert messages from queue

    First connects to TimescaleDB to insert messages from the queue.
    This happens in multiple threads.
    """

    def __init__(self, connection_string: str, table_name: str, plugin_name: str):
        """Init the DB_connector class

        Uses global EventHubBackup.message_queue as queue.

        Args:
            connection_string: connection_string for database in format:
                "dbname=... user=... password=... host=... port=..."
            table_name: name of the db table to write the data to

        """

        # import EventHubBackup to get global message_queue, not possible on top because of circular import
        from .EventHubBackup import message_queue

        self._queue = message_queue
        self._connection_string = connection_string
        self._table_name = table_name
        self._plugin_name = plugin_name

    def __enter__(self):
        self._db_controller = DB_Controller(self._connection_string)
        self._plugin = Plugin_Loader.load(class_name=self._plugin_name)

    def __exit__(self, type, value, traceback):
        self._db_controller.close()

    
    def _process_queue(self):
        """Handle the message queue

        Permanently queries the message_queue for new messages from event hub.
        Every new message gets inserted into DB.
        """

        while True:
            if not self._queue.empty():
                message = self._queue.get()
                # transform message with parser plugin
                data = self._plugin.process(message)
                self._db_controller.insert(self._table_name, [data])

    def process_in_thread(self):
        thread = threading.Thread(target=self._process_queue)
        thread.daemon = True
        thread.start()