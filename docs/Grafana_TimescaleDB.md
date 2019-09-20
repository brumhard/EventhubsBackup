# Grafana

## Examples

```SQL
SELECT
  $__time("time"),
  status_code,
  CAST(response->'lel' AS int) as testing
FROM
  testing
```

```SQL  
SELECT
  time as "time",
  COALESCE (CAST(response->'testing' as text), CAST("deviceid" as text)) as "metric",
  status_code,
  COALESCE (CAST(response->'lel' AS int), 0) as testing
FROM
  testing
```

## JSON in Postgres

Postgres supports JSON and JSONB data types so postgres also does.
JSON stores the data as string whereas JSONB stores it as binary which allows much faster queries due to indexing support.
Therefore Postgres is just as good and performant as mongoDB at processing json data.

To access the json properties the operators `->` and `->>` are supported.  
`->` will access the json property and return it as json. So `Select rawdata->'somedata'` will return the somedata property in rawdata column.  
`->>` automatically converts the resulting data to string so `Select data->>'stringdata'` will return the values in the stringdata property as string.  

> The operators can be chained to get to deeper layers in json data.

## Implemntation in Grfana

1. Add TimescaleDB as postgreSQL data source to grafana.

2. Select it as data source and either work with graphical editor or SQL editor directly.

As seen above a time column needs to be selected either by `.. as "time"` or `$__time(...)`.  
As json can miss properties at times use `COALESCE` function to replace null values.  
Use `CAST` to convert the json string data to any supported data type.
