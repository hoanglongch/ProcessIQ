#!/usr/bin/env python3
import asyncio
import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"
INPUT_TOPIC = "raw_factory_metrics"
OUTPUT_TOPIC = "validated_factory_metrics"

def validate_metric(metric: dict) -> bool:
    temp = metric.get("temperature")
    pressure = metric.get("pressure")
    if temp is None or pressure is None:
        return False
    if not (0 <= temp <= 1000):
        return False
    if not (0 <= pressure <= 5000):
        return False
    return True

async def consume_and_validate():
    consumer = AIOKafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id="validator-group"
    )
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

    await consumer.start()
    await producer.start()
    print("Validator service started, consuming raw_factory_metrics...")

    try:
        async for msg in consumer:
            try:
                metric = json.loads(msg.value.decode('utf-8'))
                if validate_metric(metric):
                    await producer.send_and_wait(
                        OUTPUT_TOPIC,
                        json.dumps(metric).encode('utf-8')
                    )
            except Exception as e:
                # In production, handle errors properly (logging, metrics, etc.)
                print("Error processing message:", e)
    finally:
        await consumer.stop()
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(consume_and_validate())