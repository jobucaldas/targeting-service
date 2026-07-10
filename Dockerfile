from docker.io/python:3.12.13-alpine3.24 as builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev postgresql-dev python3-dev

COPY requirements.txt .
RUN python -m venv /venv \
&& /venv/bin/pip install --no-cache-dir -r requirements.txt

from docker.io/python:3.12.13-alpine3.24

WORKDIR /app

RUN apk add --no-cache postgresql-libs # Necessario para o psycopg2 não dar erro

RUN addgroup -S targeting-service \
 && adduser -S targeting-service -G targeting-service
USER targeting-service

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY --chown=targeting-service app.py .
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8003} app:app"]
