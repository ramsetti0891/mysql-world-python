
import os
import time
import mysql.connector
from mysql.connector import Error

for attempt in range(10):
    try:
        connection = app.connector.connect(
            host="db",  # MySQL service name in Docker Compose
            port=3306,
            user="root",
            password="example123",
            database="company"
        )

        if connection.is_connected():
            print("Connected to MySQL successfully!")

            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")

            result = cursor.fetchone()
            print("MySQL version:", result[0])
            break

    except Error as e:
        if attempt == 9:
            print("Connection failed:", e)
        else:
            print("Waiting for MySQL...")
            time.sleep(3)

    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()
