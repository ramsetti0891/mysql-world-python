import os
from pathlib import Path

import mysql.connector
from fastapi import FastAPI, HTTPException, Query
from mysql.connector import Error


APP_ENV = os.getenv("APP_ENV", "development").lower()
app = FastAPI(
    title="Classic Models API",
    version="1.0.0",
    debug=APP_ENV == "development",
)

CUSTOMER_COLUMNS = (
    "customerNumber, customerName, contactLastName, contactFirstName, phone, "
    "addressLine1, addressLine2, city, state, postalCode, country, "
    "salesRepEmployeeNumber, creditLimit"
)


def get_connection():
    password_file = os.getenv("MYSQL_PASSWORD_FILE")
    password = (
        Path(password_file).read_text(encoding="utf-8").strip()
        if password_file
        else os.getenv("MYSQL_PASSWORD")
    )
    user = os.getenv("MYSQL_USER")
    if not user or not password:
        raise RuntimeError("MYSQL_USER and a database password must be configured")
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=user,
        password=password,
        database=os.getenv("MYSQL_DATABASE", "classicmodels"),
    )


@app.get("/health/live", include_in_schema=False)
def liveness():
    return {"status": "ok"}


@app.get("/health/ready", include_in_schema=False)
def readiness():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return {"status": "ready"}
    except Error as error:
        raise HTTPException(status_code=503, detail="Database unavailable") from error
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


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


if __name__ == "__main__":
    import uvicorn

    certfile = os.getenv("SSL_CERTFILE")
    keyfile = os.getenv("SSL_KEYFILE")
    if bool(certfile) != bool(keyfile):
        raise RuntimeError("Set both SSL_CERTFILE and SSL_KEYFILE to enable HTTPS")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        ssl_certfile=certfile,
        ssl_keyfile=keyfile,
    )
