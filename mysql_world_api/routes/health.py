from fastapi import APIRouter, HTTPException
from mysql.connector import Error

from mysql_world_api.database import database_cursor


router = APIRouter(tags=["health"])


@router.get("/health/live", include_in_schema=False)
def liveness():
    return {"status": "ok"}


@router.get("/health/ready", include_in_schema=False)
def readiness():
    try:
        with database_cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Error as error:
        raise HTTPException(status_code=503, detail="Database unavailable") from error
    return {"status": "ready"}
