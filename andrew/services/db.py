import os
import sqlite3


class SqliteDB:

    def __init__(self, andrew):
        self.andrew = andrew
        self.db_path = os.path.join(
            self.andrew.config.get('STORAGE_PATH', 'storage'),
            '{}.sqlite'.format(self.andrew.config.get('SQLITE_PATH', 'default'))
        )
        self._db_connection = self._get_connection()
        self._db_cursor = self._db_connection.cursor()
        self.check_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self._db_connection.rollback()
        else:
            self._db_connection.commit()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def check_db(self):
        tables = self._db_cursor.execute('SELECT name FROM sqlite_master')
        if not tables.fetchall():
            self._db_cursor.execute(
                'CREATE TABLE random(user_id INTEGER, username TEXT, created DATETIME, message TEXT, UNIQUE(message));'
            )

    def insert_message(self, context):
        self._db_cursor.execute(
            "INSERT or IGNORE INTO random VALUES('{user_id}', '{username}', '{created}', '{message}')".format(**context)
        )

    def get_random_message(self):
        row = self._db_cursor.execute(
            'SELECT message from random ORDER BY RANDOM() LIMIT 1;'
        ).fetchone()
        if row:
            return row[0]
        return 'The database is empty'

    def __del__(self):
        self._db_connection.close()
