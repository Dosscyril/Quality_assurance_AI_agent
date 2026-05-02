import { useState } from "react";
import Landing from "./components/Landing";
import Dashboard from "./pages/Dashboard";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

function App() {
  const [page, setPage] = useState("landing");

  const [url, setUrl] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const runTest = async (goal = "explore") => {
    if (!url) {
      alert("Please enter a URL");
      return;
    }

    setLoading(true);
    setData(null);

    try {
      const response = await fetch(`${API_URL}/run-agent`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url.trim(),
          max_steps: 3,
          goal,
        }),
      });

      if (!response.ok) throw new Error("Server error");

      const result = await response.json();
      setData(result);
    } catch (err) {
      console.error(err);
      alert("Backend error");
    }

    setLoading(false);
  };

  if (page === "landing") {
    return <Landing onStart={() => setPage("dashboard")} />;
  }

  return (
    <Dashboard
      url={url}
      setUrl={setUrl}
      data={data}
      loading={loading}
      runTest={runTest}
    />
  );
}

export default App;