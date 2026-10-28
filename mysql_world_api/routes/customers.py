from fastapi import APIRouter, HTTPException, Query
from mysql.connector import Error

from mysql_world_api.repositories import customers as customer_repository


router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("")
def list_customers(limit: int = Query(default=100, ge=1, le=500)):
    """Return customers from the classicmodels database."""
    try:
        return customer_repository.list_customers(limit)
    except Error as error:
        raise HTTPException(status_code=503, detail="Database unavailable") from error


@router.get("/first")
def first_customer():
    """Return the first customer, matching the original query."""
    try:
        customer = customer_repository.get_first_customer()
    except Error as error:
        raise HTTPException(status_code=503, detail="Database unavailable") from error

    if customer is None:
        raise HTTPException(status_code=404, detail="No customers found")
    return customer
