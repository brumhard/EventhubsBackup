# TimescaleDB

## General

- Extension on top of PostgreSQL
- can be installed on any existing PostgreSQL DB
- supports SQL natively
- extends normal SQL with functions to improve working with timeseries data
- supports all third party tools for PostgreSQL

## Why preferred

- Supports all data types (unlike InfluxDB for example)
- Classic SQL as query language (no new lang to learn)
- solid storage engine (by postgre)
- As cardinality of data increases, the performance of Timescale becomes way better than InfluxDB

## Setup

- [TimescaleDB Developer Docs: Getting Started](https://docs.timescale.com/latest/getting-started)
- setup using docker

```bash
docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg11
```

- connect to psql (`docker exec -it timescaledb psql -U postgres`)
- create new database (`CREATE database tutorial;`)
- connect to db (`\c tutorial` or later `docker exec -it timescaledb psql -U postgres -d tutorial`)
- enable extension (`CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;`)

## Hypertables

- one table from user perspective, many tables under the hood (chunks)
- partition data into one or multiple dimensions by time, key
- can be used like standard SQL table
- standard schema with at least one column specifying a time value (timestamp, int, date ...)
- creation:

```SQL
CREATE TABLE (...)
SELECT create_hypertable('<tablename>, <time-holding column>')
```
