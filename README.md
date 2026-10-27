# mysql-world-python

A FastAPI read API for the MySQL `classicmodels` database. The Compose setup
builds an immutable API image, runs API containers as a non-root user, checks
database/API readiness, and places Nginx in front of scaled API replicas.

## Run with Docker Compose

The project has `.env.dev`, `.env.test`, and `.env.prod` configuration files.
They contain non-sensitive settings only; passwords remain in separate secret
files, which are ignored by Git. Create a local development certificate and
secrets if you have not already:

```sh
mkdir -p certs secrets
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout certs/server.key -out certs/server.crt -days 365 \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
openssl rand -hex 32 > secrets/mysql_root_password.txt
openssl rand -hex 32 > secrets/mysql_app_password.txt
chmod 600 certs/server.key secrets/*.txt
```

For your existing development database volume, keep the current value in
`secrets/mysql_root_password.txt`; do not replace it with a new random password
unless you also rotate the database root password.

For an existing MySQL data volume, `mysql_root_password.txt` must contain the
current MySQL root password. MySQL only reads initialization settings on the
first creation of its data directory. The API account init script also only
runs for a new volume. For an existing volume, create the API user once by
connecting as root and running the SQL below, substituting the contents of
`secrets/mysql_app_password.txt` for `<APP_PASSWORD>`:

```sql
CREATE USER IF NOT EXISTS 'classicmodels_api'@'%' IDENTIFIED BY '<APP_PASSWORD>';
ALTER USER 'classicmodels_api'@'%' IDENTIFIED BY '<APP_PASSWORD>';
GRANT SELECT ON classicmodels.* TO 'classicmodels_api'@'%';
```

Build and start three API replicas:

```sh
docker compose --env-file .env.dev up -d --build --scale web=3
```

Open `https://localhost/docs`. Nginx terminates HTTPS and load balances API
requests. The self-signed certificate is for local use, so browsers will show a
warning. `curl -k https://localhost/customers?limit=5` can be used for a local
check; do not disable certificate verification for a public service. Ports 80
and 443 must be available. Scale later with, for example,
`docker compose --env-file .env.dev up -d --scale web=5`.

Each environment uses a separate Compose project name and database volume. The
test and production profiles also use separate secret paths. Create their
secrets before starting those environments:

```sh
openssl rand -hex 32 > secrets/test_mysql_root_password.txt
openssl rand -hex 32 > secrets/test_mysql_app_password.txt
openssl rand -hex 32 > secrets/prod_mysql_root_password.txt
openssl rand -hex 32 > secrets/prod_mysql_app_password.txt
chmod 600 secrets/*.txt
```

Start the isolated test environment with
`docker compose --env-file .env.test up -d --build --scale web=1`. It creates an
empty `classicmodels_test` database; load test fixtures before exercising the
customer routes. The production profile is started with
`docker compose --env-file .env.prod up -d --build --scale web=3`; place a
trusted `server.crt` and `server.key` in the configured `certs-prod` directory
and configure `nginx.conf` for the public hostname before exposing it.

The MySQL service is not published on the host. Use `docker compose exec db ...`
for administration. The database image creates the `classicmodels` database,
but does not seed its sample tables or rows; import your Classic Models SQL dump
separately if they are not already present.

## Local development

Create a virtual environment, install the pinned dependencies, and configure
database credentials before starting the API:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
set -a
. ./.env.dev
set +a
MYSQL_HOST=127.0.0.1 MYSQL_PASSWORD_FILE=secrets/mysql_app_password.txt \
  SSL_CERTFILE=certs/server.crt SSL_KEYFILE=certs/server.key PORT=8443 python app.py
```

This requires a MySQL server reachable from the host on port 3306. The API also
serves `/customers`, `/customers/first`, `/health/live`, and `/health/ready`.
Interactive API docs are at `/docs`.

## Deployment notes

This Compose configuration is intended for a single Docker host. For a public
deployment, replace the local certificate with one trusted by clients and valid
for the public hostname. Store secrets in the deployment platform's secret
manager, pin container images by digest, and configure backups, monitoring, and
network access for your environment.
