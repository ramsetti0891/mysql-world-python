# mysql-world-python

A small REST API for reading customers from the MySQL `classicmodels` database.

## Run with Docker Compose

```sh
docker compose up
```

The API listens on `http://localhost:8000`:

- `GET /customers` returns up to 100 customers. Set `?limit=25` to choose a limit (1–500).
- `GET /customers/first` returns the first customer, matching the original query.
- `GET /docs` opens the interactive API documentation.

The API reads database connection settings from `MYSQL_HOST`, `MYSQL_PORT`,
`MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE`. Defaults are suitable for
the provided Compose configuration.

## Run locally

Install the API dependencies and start the server:

```sh
python -m pip install fastapi uvicorn mysql-connector-python
uvicorn app:app --reload
```

Set the `MYSQL_*` environment variables if MySQL is not available at the default
local connection settings.
