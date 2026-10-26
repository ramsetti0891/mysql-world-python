import os

import mysql.connector
from fastapi import FastAPI, HTTPException, Query
from mysql.connector import Error


app = FastAPI(title="Classic Models API", version="1.0.0")

CUSTOMER_COLUMNS = (
    "customerNumber, customerName, contactLastName, contactFirstName, phone, "
    "addressLine1, addressLine2, city, state, postalCode, country, "
    "salesRepEmployeeNumber, creditLimit"
)


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "example123"),
        database=os.getenv("MYSQL_DATABASE", "classicmodels"),
    )


@app.get("/customers")
def list_customers(limit: int = Query(default=100, ge=1, le=500)):
    """Return customers from the classicmodels database."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            f"SELECT {CUSTOMER_COLUMNS} FROM customers ORDER BY customerNumber LIMIT %s",
            (limit,),
        )
        return cursor.fetchall()
    except Error as error:
        raise HTTPException(status_code=503, detail="Database unavailable") from error
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


@app.get("/customers/first")
def first_customer():
    """Return the first customer, matching the original app query."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            f"SELECT {CUSTOMER_COLUMNS} FROM customers ORDER BY customerNumber LIMIT 1"
        )
        customer = cursor.fetchone()
        if customer is None:
            raise HTTPException(status_code=404, detail="No customers found")
        return customer
    except Error as error:
        raise HTTPException(status_code=503, detail="Database unavailable") from error
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
