# Event Hubs Backup

## Getting started

### Prerequisites

> The whole code is documented by docstrings and inline comments. Refer to these to get a deep understanding.

- Python 3 (docker?)
- Azure Event Hubs namespace and hub
- [Azure Block Blob storage account](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-create-account-block-blob) with container
- Running TimescaleDB ([Setup](https://docs.timescale.com/latest/getting-started/installation)/ See below) with table that support the plugins output.
- Parser plugin for the messages in that eventhub available in the plugin folder

> Foreach event hub, you need one seperate storage container to save checkpoints.

### Config file

#### Location

> Currently the below isn't implemented, change in `app.py`

The following locations are checked in order

1. Value of environment variable `$EH_READER_CONFIG` as path
2. Home directory (linux: `~/eh_reader_config.yml`, windows: `$HOMEPATH\eh_reader_config.yml`)
3. Current directory (`./eh_reader_config.yml`)
4. linux: `/etc/monitoring/eh_reader_config.yml` or  windows: `C:\monitoring\eh_reader_config.yml`

#### Structure

```yml
DB_connection_string: "<timescale db connection string>"
EH_connection_string: "<event hub connection string>"
SA_connection_string: "<storage account connection string>"
SA_container_name: "<storage account container name"
DB_writer_count: <number of threads that write to db>
```

Expected connection string formats:

DB_connection_string:

- `"dbname=<name of db> user=<db user> password=<password for db user> host=<host of db> port=<db port>"`
- by default the user is `postgres` and port is `5432`

EH_connection_string:

- first part: [look here](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-get-connection-string#get-connection-string-from-the-portal)
- add `";EntityPath=<name of service hub>"`
- resulting: `"Endpoint=...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=..."`

SA_connection_string:

- [Get connection string from portal](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-manage#view-account-keys-and-connection-string)

### Usage

1. Create config file (see above)

2. run `pip install -r requirements.txt`

> `requirements.txt` currently includes `pylint` and `black` as formatter

3. Change the default path in app.py (you can also use the command line to pass the full path)

4. Run app.py and enjoy!

## TODO

- implement a config file finder (search different paths as shown in the above definition)
- create plugins for all formats that should be supported
- clean up requirements?
