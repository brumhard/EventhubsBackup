# TSDB options for healthcheck

## Sources

- [4 Best Time Series Databases To Watch in 2019](https://medium.com/schkn/4-best-time-series-databases-to-watch-in-2019-ef1e89a72377)
- ...

## Promethues

not fitting as the sdk doesn't support to set the timestamps yourself
see Prometheus.md

## Influx

\+ open source
\+ supports setting custom timestamps 
\+ works with concurrency
\+ good docs
\- costs for horizontal scaling (InfluxEnterprise)
\+ direct data source support by grafana
\+ supports all data types ([InfluxDB Python](https://influxdb-python.readthedocs.io/en/latest/examples.html))
\+ supports json as input

## TimescaleDB

[TimescaleDB 101: the why, what, and how - Aiven - Medium](https://medium.com/@aiven_io/timescaledb-101-the-why-what-and-how-9c0eb08a7c0b)
\+ supports SQL (extension for PostgreSQL)-> supports custom timestamps/ all data types
\- but needs schema
\- no real sdk in that sense, write PostgreSQL commands to extract data
\+ supports grafana through postgres query editor
\+ open source with enterprise add ons as an option

## OpenTSDB

\+ great performance
\- no official python sdk (only [http api](http://opentsdb.net/docs/build/html/api_http/))
\+ direct support by grafana
\- doesn't seem to support more than numeric values ([/api/put — OpenTSDB 2.3 documentation](http://opentsdb.net/docs/build/html/api_http/put.html), [Writing Data — OpenTSDB 2.3 documentation](http://opentsdb.net/docs/build/html/user_guide/writing/))

## Graphite

\- only supports numeric data ([Overview — Graphite 1.1.5 documentation](https://graphite.readthedocs.io/en/latest/overview.html))
\- no official python sdk

## Kairos DB

\- no python sdk only api ([kairosdb/kairosdb-examples-python](https://github.com/kairosdb/kairosdb-examples-python))
\- custom data requires coding effort [Custom Data — KairosDB 1.0.1 documentation](https://kairosdb.github.io/docs/build/html/kairosdevelopment/CustomData.html)

## -> InfluxDB vs TimescaleDB

[TimescaleDB vs. InfluxDB: Purpose built differently for time-series data](https://blog.timescale.com/blog/timescaledb-vs-influxdb-for-time-series-data-timescale-influx-sql-nosql-36489299877/)

### Datamodel

- Timescale: SQL schema -> complete freedom about datatypes, SQL with some improvements as query language
- Influx: nosql -> set of allowed datatype and values (tags and fields), custom query language

### Reliability

- Timescale: based on PostgreSQL -> way more tools
- Influx: custom storage engine

### Performance

As cardinality of data increases, the performance of Timescale becomes way better than InfluxDB

[Which Time-Series Database is Better: TimescaleDB vs InfluxDB \| Severalnines](https://severalnines.com/database-blog/which-time-series-database-better-timescaledb-vs-influxdb)
