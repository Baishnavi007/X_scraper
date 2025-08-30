import { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000"; // backend URL

function App() {
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch latest trend from DB
  async function fetchTrends() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/api/latest-trends/`);
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const data = await res.json();
      setTrends(data);
    } catch (err) {
      setError(err.message);
      setTrends(null);
    } finally {
      setLoading(false);
    }
  }

  // Scrape & save new trend
  async function scrapeSaveTrend() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/api/scrape-save-trend/`, { method: "POST" });
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const data = await res.json();
      setTrends(data);
    } catch (err) {
      setError(err.message);
      setTrends(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-container">
      <h1>X Trending Topics</h1>

      <div className="buttons">
        <button onClick={fetchTrends}>Fetch Latest Trends</button>
        <button onClick={scrapeSaveTrend}>Scrape & Save Trend</button>
      </div>

      {loading && <p className="loading">Loading...</p>}
      {error && <p className="error">Error: {error}</p>}

      {trends && (
        <div className="trends-container">
          <small>ID: {trends.id}</small>

          <ol>
            <li>{trends.trend1}</li>
            <li>{trends.trend2}</li>
            <li>{trends.trend3}</li>
            <li>{trends.trend4}</li>
            <li>{trends.trend5}</li>
          </ol>

          <p>
            <b>Scraped At:</b> {new Date(trends.scraped_at).toLocaleString()}
          </p>
          <p>
            <b>IP Address:</b> {trends.ip_address}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
