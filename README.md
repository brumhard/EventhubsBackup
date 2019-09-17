# Event Hubs Backup

## Getting started

### Prerequisites

- Python 3 (docker?)
- Azure Event Hubs namespace and hub
- [Azure Block Blob storage account](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-create-account-block-blob) with container
- Running TimescaleDB ([Setup](https://docs.timescale.com/latest/getting-started/installation)/ See below)

### Config file

#### Location

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

---

## TimescaleDB

### General

- Extension on top of PostgreSQL
- can be installed on any existing PostgreSQL DB
- supports SQL natively
- extends normal SQL with functions to improve working with timeseries data
- supports all third party tools for PostgreSQL

### Why preferred

- Supports all data types (unlike InfluxDB for example)
- Classic SQL as query language (no new lang to learn)
- solid storage engine (by postgre)
- As cardinality of data increases, the performance of Timescale becomes way better than InfluxDB

### Setup

- [TimescaleDB Developer Docs: Getting Started](https://docs.timescale.com/latest/getting-started)
- setup using docker

```bash
docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg11
```

- connect to psql (`docker exec -it timescaledb psql -U postgres`)
- create new database (`CREATE database tutorial;`)
- connect to db (`\c tutorial` or later `docker exec -it timescaledb psql -U postgres -d tutorial`)
- enable extension (`CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;`)

### Hypertables

- one table from user perspective, many tables under the hood (chunks)
- partition data into one or multiple dimensions by time, key
- can be used like standard SQL table
- standard schema with at least one column specifying a time value (timestamp, int, date ...)
- creation:

```SQL
CREATE TABLE (...)
SELECT create_hypertable('<tablename>, <time-holding column>')
```
