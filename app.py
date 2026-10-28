"""Compatibility entry point for running the API with ``python app.py``."""

import os

from mysql_world_api.main import app


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
