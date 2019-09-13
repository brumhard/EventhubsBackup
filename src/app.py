from db_connector import DB_Connector
import yaml
import json
import datetime
import argparse

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


data_to_insert = [
    {
        "time": datetime.datetime.now(),
        "deviceid": 7,
        "status_code": 400,
        "response": json.dumps({"testing": "lul"}),
    }
]

db = DB_Connector(config_data["DB_connection_string"])
with db:
    db.insert("testing", data_to_insert)

