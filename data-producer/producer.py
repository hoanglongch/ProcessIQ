#!/usr/bin/env python3
import time
import json
import random
import logging
from kafka import KafkaProducer
from typing import Dict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "raw_factory_metrics"

def generate_fake_metric() -> Dict:
    """
    Generates a random sensor metric.
    """
    return {
        "sensor_id": "sensor-" + str(random.randint(1, 5)),
        "temperature": random.uniform(0, 1000),
        "pressure": random.uniform(0, 5000),
        "timestamp": int(time.time() * 1000)
    }

def main():
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    logging.info(f"Starting to send messages to Kafka topic '{TOPIC}'...")
    while True:
        try:
            metric = generate_fake_metric()
            producer.send(TOPIC, json.dumps(metric).encode("utf-8"))
            producer.flush()
            logging.info(f"Sent metric: {metric}")
            time.sleep(1)  # 1-second interval
        except Exception as e:
            logging.error(f"Error sending metric to Kafka: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    main()