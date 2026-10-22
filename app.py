import os
import time
import mysql.connector
from mysql.connector import Error

for attempt in range(5):
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=3306,
            user="root",
            password="example123",
            database="classicmodels"
        )

        if connection.is_connected():
            print("Connected to MySQL successfully!")

            cursor = connection.cursor()
            cursor.execute("""SELECT customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber, creditLimit
FROM classicmodels.customers
LIMIT 1""")

            result = cursor.fetchone()
            print("Customer number:", result[0])
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
