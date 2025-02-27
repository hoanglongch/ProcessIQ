package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "time"

    "github.com/segmentio/kafka-go"
    "github.com/ClickHouse/clickhouse-go"
)

// Metric represents the JSON structure of our validated messages
type Metric struct {
    SensorID    string  `json:"sensor_id"`
    Temperature float64 `json:"temperature"`
    Pressure    float64 `json:"pressure"`
    Timestamp   int64   `json:"timestamp"`
}

func main() {
    // Create a Kafka reader
    r := kafka.NewReader(kafka.ReaderConfig{
        Brokers:  []string{"localhost:9092"},
        Topic:    "validated_factory_metrics",
        GroupID:  "ingestion-service-group",
        MinBytes: 10e3,  // 10KB
        MaxBytes: 10e6,  // 10MB
    })
    defer r.Close()

    // Connect to ClickHouse
    connect, err := clickhouse.OpenDirect("tcp://127.0.0.1:9000?debug=true")
    if err != nil {
        log.Fatal(err)
    }
    defer connect.Close()

    // Create table if not exists
    createTableQuery := `
    CREATE TABLE IF NOT EXISTS factory_metrics (
        sensor_id String,
        temperature Float64,
        pressure Float64,
        timestamp UInt64
    ) ENGINE = MergeTree()
    ORDER BY (sensor_id, timestamp)
    `
    _, err = connect.Exec(createTableQuery)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println("Ingestion service started. Listening for validated metrics...")

    ctx := context.Background()
    var metricsBatch []Metric
    batchSize := 1000

    for {
        m, err := r.ReadMessage(ctx)
        if err != nil {
            log.Println("Error reading message:", err)
            continue
        }

        var metric Metric
        if err := json.Unmarshal(m.Value, &metric); err != nil {
            log.Println("Unmarshal error:", err)
            continue
        }

        metricsBatch = append(metricsBatch, metric)
        if len(metricsBatch) >= batchSize {
            insertMetrics(connect, metricsBatch)
            metricsBatch = nil
        }
    }
}

func insertMetrics(connect clickhouse.Conn, metrics []Metric) {
    tx, err := connect.Begin()
    if err != nil {
        log.Println("Transaction begin error:", err)
        return
    }
    stmt, err := tx.Prepare("INSERT INTO factory_metrics (sensor_id, temperature, pressure, timestamp) VALUES (?, ?, ?, ?)")
    if err != nil {
        log.Println("Prepare statement error:", err)
        return
    }
    defer stmt.Close()

    for _, metric := range metrics {
        _, err = stmt.Exec(
            metric.SensorID,
            metric.Temperature,
            metric.Pressure,
            metric.Timestamp,
        )
        if err != nil {
            log.Println("Exec error:", err)
        }
    }

    if err = tx.Commit(); err != nil {
        log.Println("Commit error:", err)
    } else {
        fmt.Printf("Inserted %d metrics\n", len(metrics))
    }
}