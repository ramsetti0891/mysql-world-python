FROM python:3.12.15-slim-bookworm AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /build

COPY requirements.txt .
RUN python -m pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.12.15-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home-dir /app app \
    && install -d --owner=10001 --group=10001 --mode=0700 /run/app-secrets

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && python -m pip check \
    && rm -rf /wheels

COPY --chown=app:app app.py container_entrypoint.py ./
COPY --chown=app:app mysql_world_api ./mysql_world_api

EXPOSE 8000

ENTRYPOINT ["python", "/app/container_entrypoint.py"]
CMD ["uvicorn", "mysql_world_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
