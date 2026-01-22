FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic.ini ./
COPY alembic_postgres ./alembic_postgres
COPY scripts ./scripts

CMD alembic upgrade head && \
    python -m scripts.seed.create_test_data && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
