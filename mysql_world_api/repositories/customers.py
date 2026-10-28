from typing import Optional

from mysql_world_api.database import database_cursor


CUSTOMER_COLUMNS = (
    "customerNumber, customerName, contactLastName, contactFirstName, phone, "
    "addressLine1, addressLine2, city, state, postalCode, country, "
    "salesRepEmployeeNumber, creditLimit"
)


def list_customers(limit: int) -> list[dict]:
    with database_cursor(dictionary=True) as cursor:
        cursor.execute(
            f"SELECT {CUSTOMER_COLUMNS} FROM customers ORDER BY customerNumber LIMIT %s",
            (limit,),
        )
        return cursor.fetchall()


def get_first_customer() -> Optional[dict]:
    with database_cursor(dictionary=True) as cursor:
        cursor.execute(
            f"SELECT {CUSTOMER_COLUMNS} FROM customers ORDER BY customerNumber LIMIT 1"
        )
        return cursor.fetchone()
