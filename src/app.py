"""App to write messages from event hub to TimescaleDB

Pls see Readme.md for help on usage.
"""

import yaml
import argparse
import logging
from contextlib import ExitStack
from eventhubbackuplib.EventHubBackup import EventHubBackup

logger = logging.getLogger("eventhubbackuplib")
logger.setLevel(logging.DEBUG)

eh_logger = logging.getLogger("azure.eventhub")
eh_logger.setLevel(logging.DEBUG)

log_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(log_format)
logger.addHandler(handler)
eh_logger.addHandler(handler)

logger.info(__name__)

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

eh_backup = EventHubBackup(
    db_writer_count=config_data["DB_writer_count"],
    db_connection_string=config_data["DB_connection_string"],
    db_table_name=config_data["DB_table_name"],
    plugin_name=config_data["Plugin_name"],
    eh_connection_string=config_data["EH_connection_string"],
    sa_connection_string=config_data["SA_connection_string"],
    sa_container_name=config_data["SA_container_name"],
)

eh_backup.start()
