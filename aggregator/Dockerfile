FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY aggregator.py ./

ENV CLICKHOUSE_HOST=clickhouse
ENV CLICKHOUSE_USER=default
ENV CLICKHOUSE_PASS=""
ENV CLICKHOUSE_DB=default

EXPOSE 8000

CMD ["uvicorn", "aggregator:app", "--host", "0.0.0.0", "--port", "8000"]