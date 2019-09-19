"""App to write messages from event hub to TimescaleDB

Pls see Readme.md for help on usage.
"""


from event_processing import Event_Processing
from messaging import EventHub_Receiver
import queue
import yaml
import json
import datetime
import argparse
import logging
from contextlib import ExitStack

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# arguments for script
parser = argparse.ArgumentParser(
    description="Write messages from event hub to database."
)
parser.add_argument(
    "-t",
    "--targetfile",
    help="Path to the config file.",
    default="C:\\Users\\brumhardadm\\Desktop\\tmp\\eh_reader_config.yml",  # , required=True
)
args = parser.parse_args()

# open external config file
with open(args.targetfile, "r") as config_file:
    config_data = yaml.safe_load(config_file)

# open queue for exchange of messages between threads
message_queue = queue.Queue()

# use ExitStack to close all db connections in the end
with ExitStack() as stack:
    for i in range(0, config_data["DB_writer_count"]):
        db = Event_Processing(
            config_data["DB_connection_string"],
            config_data["DB_table_name"],
            config_data["Plugin_name"],
        )
        stack.enter_context(db)
        db.process_in_thread()

    receiver = EventHub_Receiver(
        config_data["EH_connection_string"],
        config_data["SA_connection_string"],
        config_data["SA_container_name"],
    )
    with receiver:
        receiver.receive_messages()

