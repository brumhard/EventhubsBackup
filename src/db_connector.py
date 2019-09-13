import psycopg2
import datetime
import json


class DB_Connector:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def __enter__(self):
        self._conn = psycopg2.connect(self.connection_string)
        self._cur = self._conn.cursor()

    def __exit__(self, type, value, traceback):
        if self._conn:
            self._cur.close()
            self._conn.close()

    def insert(self, table_name: str, data_to_insert: list):
        # make sure every entry in data_to_insert has same keys
        keys_sets = list(map(lambda x: list(x.keys()), data_to_insert))
        for key_set in keys_sets[1:]:
            if key_set != keys_sets[0]:
                raise ValueError("Every dict in list should have same keys")

        column_names = ", ".join(keys_sets[0])
        values_placeholder = ("%s, " * len(keys_sets[0])).rstrip(", ")
        values_to_insert = list(map(lambda x: list(x.values()), data_to_insert))
        sql_insert = (
            f"INSERT INTO {table_name} ({column_names}) values ({values_placeholder})"
        )
        self._cur.executemany(sql_insert, values_to_insert)
        self._conn.commit()
