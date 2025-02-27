import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

// Basic Auth credentials (MUST match aggregator!)
const USERNAME = "admin";
const PASSWORD = "secret";

function PressureChart() {
  const [pressureData, setPressureData] = useState([]);
  const [sensorId, setSensorId] = useState("sensor-1");

  useEffect(() => {
    async function fetchPressure() {
      try {
        const resp = await fetch(`http://localhost:8000/metrics/by-sensor/${sensorId}`, {
          headers: {
            Authorization: "Basic " + btoa(USERNAME + ":" + PASSWORD),
          },
        });
        if (!resp.ok) {
          throw new Error(`Error fetching sensor data: ${resp.status}`);
        }
        const data = await resp.json();
        // Reverse to get chronological order from oldest to newest
        const reversed = [...data].reverse();
        setPressureData(reversed);
      } catch (error) {
        console.error("Error fetching sensor-specific data:", error);
      }
    }

    fetchPressure();
    const interval = setInterval(fetchPressure, 5000);
    return () => clearInterval(interval);
  }, [sensorId]);

  return (
    <div className="mt-8">
      <div className="flex items-center mb-2">
        <label htmlFor="sensor-select" className="mr-2 font-semibold">
          Choose Sensor:
        </label>
        <select
          id="sensor-select"
          value={sensorId}
          onChange={(e) => setSensorId(e.target.value)}
          className="border rounded p-1"
        >
          <option value="sensor-1">sensor-1</option>
          <option value="sensor-2">sensor-2</option>
          <option value="sensor-3">sensor-3</option>
          <option value="sensor-4">sensor-4</option>
          <option value="sensor-5">sensor-5</option>
        </select>
      </div>
      <LineChart width={600} height={300} data={pressureData} className="mx-auto">
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="pressure" stroke="#ff7300" />
      </LineChart>
    </div>
  );
}

export default PressureChart;