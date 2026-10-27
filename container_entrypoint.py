import os
import sys
from pathlib import Path


APP_UID = 10001
APP_GID = 10001
RUNTIME_SECRET = Path("/run/app-secrets/mysql_app_password")


def main():
    secret_source = os.getenv("MYSQL_PASSWORD_FILE")
    if not secret_source:
        raise RuntimeError("MYSQL_PASSWORD_FILE must be configured")

    secret_value = Path(secret_source).read_bytes()
    if not secret_value.strip():
        raise RuntimeError("The database password secret is empty")

    RUNTIME_SECRET.write_bytes(secret_value)
    os.chown(RUNTIME_SECRET, APP_UID, APP_GID)
    os.chmod(RUNTIME_SECRET, 0o400)
    os.environ["MYSQL_PASSWORD_FILE"] = str(RUNTIME_SECRET)

    os.setgid(APP_GID)
    os.setuid(APP_UID)
    os.execvp(sys.argv[1], sys.argv[1:])


if __name__ == "__main__":
    main()
