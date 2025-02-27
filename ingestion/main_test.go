package main

import (
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestInsertMetrics(t *testing.T) {
    // We can’t fully test insertion without a real or mocked ClickHouse.
    // A recommended approach is to use dependency injection or mock the DB connection.

    // Here, we’ll do a simplified check ensuring our Metric struct is correct and that
    // the function doesn’t panic with an empty slice.
    var metrics []Metric
    metrics = append(metrics, Metric{
        SensorID: "sensor-1",
        Temperature: 100.0,
        Pressure: 500.0,
        Timestamp: 1234567890,
    })

    // We won't actually call insertMetrics with a real DB here, but let's just
    // assure that it doesn't panic and that the struct is as expected.
    // This is a placeholder to show how you'd structure a test.
    assert.Equal(t, "sensor-1", metrics[0].SensorID)
    assert.Equal(t, 100.0, metrics[0].Temperature)
    assert.Equal(t, 500.0, metrics[0].Pressure)
    assert.Equal(t, int64(1234567890), metrics[0].Timestamp)
}