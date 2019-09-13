from db_connector import DB_Connector
import json
import datetime

data_to_insert = [
    {
        "time": datetime.datetime.now(),
        "deviceid": 3,
        "status_code": 400,
        "response": json.dumps({"testing": "lul"}),
    },
    {
        "time": datetime.datetime.now(),
        "deviceid": 4,
        "status_code": 240,
        "response": json.dumps({"testing": "lul"}),
    },
]

db = DB_Connector(
    "dbname=tutorial user=postgres password=dbtestingpw host=52.136.208.141 port=5432"
)
with db:
    db.insert("testing", data_to_insert)

