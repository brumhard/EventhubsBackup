import psycopg2
import datetime
import json
import threading
 
class DB_Controller:
    def __init__(self, connection_string):
        """Init the DB_controller class

        Used as interface for PostgreSQL DBs to insert rows and handle connection.

        Args:
            connection_string: connection_string for database in format:
                "dbname=... user=... password=... host=... port=..."
        """
        self.connection_string = connection_string
        self._conn = psycopg2.connect(self.connection_string)
        self._cur = self._conn.cursor()
    
    def close(self):
        if self._conn:
            self._cur.close()
            self._conn.close()

    def insert(self, table_name: str, data_to_insert: list):
        """ Insert into table

        Uses keys from a the data_to_insert dict as column names
        and values as their values to be easily usable with json data.

        Args:
            table_name (str): The name of the database table where the
                data is to be inserted.
            data_to_insert (list): List of data dicts to insert. 
                Keys are column names, values are values.
        
        Raises:
            ValueError: If data_to_insert contains dicts with different keys.
        """

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

