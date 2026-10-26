# mysql-world-python

A small REST API for reading customers from the MySQL `classicmodels` database.

## Run with Docker Compose

Create a self-signed certificate for local development before starting Compose:

```sh
mkdir -p certs
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout certs/server.key -out certs/server.crt -days 365 \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

Then start the API and database:

```sh
docker compose up -d --scale web=3
```

Nginx listens on HTTPS port 443 and balances requests across the `web` replicas.
Open `https://localhost/docs`. Port 80 redirects to HTTPS. The self-signed
certificate is for development, so browsers will show a warning. For example,
`curl -k https://localhost/customers?limit=5` skips certificate verification for
a local check. Do not use `-k` with a public service.

To change the replica count later, run `docker compose up -d --scale web=5` (or
choose another count). The replicas are internal to the Compose network; clients
connect through the single Nginx address.

- `GET /customers` returns up to 100 customers. Set `?limit=25` to choose a limit (1–500).
- `GET /customers/first` returns the first customer, matching the original query.
- `GET /docs` opens the interactive API documentation over HTTPS.

The API reads database connection settings from `MYSQL_HOST`, `MYSQL_PORT`,
`MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE`. Defaults are suitable for
the provided Compose configuration. Nginx uses the certificate and key at
`certs/server.crt` and `certs/server.key`.

## Run locally

Install the API dependencies and start the server:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
SSL_CERTFILE=certs/server.crt SSL_KEYFILE=certs/server.key PORT=8443 python app.py
```

Set the `MYSQL_*` environment variables if MySQL is not available at the default
local connection settings. For a public deployment, configure a certificate
trusted by clients and valid for the hostname they use; the self-signed
development certificate is not suitable for public HTTPS.
