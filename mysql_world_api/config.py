import os
from pathlib import Path


APP_ENV = os.getenv("APP_ENV", "development").lower()


def mysql_settings() -> dict[str, object]:
    password_file = os.getenv("MYSQL_PASSWORD_FILE")
    password = (
        Path(password_file).read_text(encoding="utf-8").strip()
        if password_file
        else os.getenv("MYSQL_PASSWORD")
    )
    user = os.getenv("MYSQL_USER")
    if not user or not password:
        raise RuntimeError("MYSQL_USER and a database password must be configured")

    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": user,
        "password": password,
        "database": os.getenv("MYSQL_DATABASE", "classicmodels"),
    }
