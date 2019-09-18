"""App to write messages from event hub to TimescaleDB

Pls see Readme.md for help on usage.
"""


from db_connector import DB_Connector
from messaging import Async_EventHub_Connector
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
        db = DB_Connector(config_data["DB_connection_string"], config_data["DB_table_name"])
        stack.enter_context(db)
        db.process_in_thread()

    receiver = Async_EventHub_Connector(
        config_data["EH_connection_string"],
        config_data["SA_connection_string"],
        config_data["SA_container_name"],
    )
    with receiver:
        receiver.receive_messages()

