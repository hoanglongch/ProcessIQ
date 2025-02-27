#!/usr/bin/env python3
from fastapi import FastAPI
import uvicorn
from clickhouse_driver import Client

app = FastAPI()
client = Client(host="127.0.0.1", user="default", password="", database="default")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics/summary")
def metrics_summary():
    # Example query: last hour of data
    query = """
    SELECT
        sensor_id,
        AVG(temperature) as avg_temp,
        AVG(pressure) as avg_pressure,
        COUNT(*) as samples
    FROM factory_metrics
    WHERE timestamp > (now() - 3600) * 1000
    GROUP BY sensor_id
    ORDER BY sensor_id
    """
    rows = client.execute(query)
    result = []
    for row in rows:
        result.append({
            "sensor_id": row[0],
            "avg_temperature": row[1],
            "avg_pressure": row[2],
            "samples": row[3]
        })
    return result

if __name__ == "__main__":
    uvicorn.run("aggregator:app", host="0.0.0.0", port=8000, reload=True)