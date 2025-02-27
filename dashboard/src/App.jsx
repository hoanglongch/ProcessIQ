import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

function App() {
  const [data, setData] = useState([]);

  // Fetch data from aggregator
  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("http://localhost:8000/metrics/summary");
        const jsonData = await res.json();
        setData(jsonData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
    fetchData();

    // Optionally, poll every 5 seconds
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Manufacturing Metrics</h1>
      <p className="text-gray-700">
        Real-time average temperature and pressure per sensor.
      </p>
      <BarChart
        width={600}
        height={300}
        data={data}
        className="mx-auto mt-6"
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="sensor_id" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="avg_temperature" fill="#8884d8" />
      </BarChart>
    </div>
  );
}

export default App;