from fastapi import FastAPI

from mysql_world_api.config import APP_ENV
from mysql_world_api.routes import customers, health


app = FastAPI(
    title="Classic Models API",
    version="1.0.0",
    debug=APP_ENV == "development",
)
app.include_router(health.router)
app.include_router(customers.router)
