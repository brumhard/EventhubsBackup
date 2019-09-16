from db_connector import DB_Connector
from messaging import Async_EventHub_Connector
import yaml
import json
import datetime
import argparse
import queue
import logging

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
    default="C:\\Users\\brumhardadm\\Desktop\\tmp\\eh_reader_config.yaml",  # , required=True
)
args = parser.parse_args()

# open external config file
with open(args.targetfile, "r") as config_file:
    config_data = yaml.safe_load(config_file)

message_queue = queue.Queue()

receiver = Async_EventHub_Connector(config_data["EH_connection_string"])
with receiver:
    receiver.receive_messages(message_queue)

# db = DB_Connector(config_data["DB_connection_string"])
# with db:
#     # db.insert("testing", data_to_insert)
#     db.process_queue(message_queue)

