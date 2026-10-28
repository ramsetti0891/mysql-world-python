from contextlib import contextmanager
from typing import Iterator

import mysql.connector

from mysql_world_api.config import mysql_settings


def get_connection():
    return mysql.connector.connect(**mysql_settings())


@contextmanager
def database_cursor(*, dictionary: bool = False) -> Iterator[object]:
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=dictionary)
        yield cursor
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            if connection.is_connected():
                connection.close()
