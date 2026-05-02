import { useState } from "react";
import Navbar from "../components/Navbar";
import ScoreChart from "../components/ScoreChart";

export default function Dashboard({ url, setUrl, data, loading, runTest }) {
  const [goal, setGoal] = useState("explore");

  // wrap original runTest to include goal
  const handleRun = () => {
    runTest(goal);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />

      <div className="p-8">

        {/* Input + Goal */}
        <div className="flex flex-wrap gap-3 mb-6 items-center">
          <input
            className="px-4 py-2 bg-gray-800 border border-gray-600 rounded w-80"
            placeholder="Enter website URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          {/* Goal Dropdown */}
          <select
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            className="bg-gray-800 px-3 py-2 rounded border border-gray-600"
          >
            <option value="explore">Explore</option>
            <option value="login">Test Login</option>
            <option value="search">Test Search</option>
          </select>

          <button
            onClick={handleRun}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded disabled:opacity-50"
          >
            {loading ? "Running..." : "Run Test"}
          </button>
        </div>

        {/* Goal Display */}
        <p className="text-sm text-gray-400 mb-4">
          🎯 Goal: <span className="text-white">{goal}</span>
        </p>

        {/* Loader */}
        {loading && (
          <div className="flex flex-col items-center mt-4">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-blue-400 mt-2">
              🤖 AI is testing your website...
            </p>
          </div>
        )}

        {/* Results */}
        {data && (
          <div className="grid md:grid-cols-2 grid-cols-1 gap-6">

            {/* Score */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-lg flex flex-col items-center">
              <h2 className="text-lg mb-2">📊 Score</h2>
              <ScoreChart score={data.score || 0} />
            </div>

            {/* Report */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-lg">
              <h2 className="text-lg mb-3">📋 Report</h2>

              {data.report?.length > 0 ? (
                data.report.map((r, i) => (
                  <div key={i} className="mb-2 text-sm">
                    <span
                      className={`px-2 py-1 text-xs rounded mr-2 ${
                        r.type === "success"
                          ? "bg-green-500 text-black"
                          : r.type === "warning"
                          ? "bg-yellow-400 text-black"
                          : "bg-red-500 text-white"
                      }`}
                    >
                      {r.type}
                    </span>
                    {r.message}
                  </div>
                ))
              ) : (
                <p className="text-gray-400">No report available</p>
              )}
            </div>

            {/* Agent Actions */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-lg col-span-2">
              <h2 className="text-lg mb-3">🤖 Agent Actions</h2>

              {data.agent_findings?.length > 0 ? (
                data.agent_findings.map((a, i) => (
                  <div
                    key={i}
                    className="bg-gray-700/40 px-3 py-2 rounded mb-2 text-sm"
                  >
                    🔹 Step {i + 1}: {a}
                  </div>
                ))
              ) : (
                <p className="text-gray-400">No agent actions recorded</p>
              )}
            </div>

            {/* Screenshot */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-lg col-span-2">
              <h2 className="text-lg mb-3">📸 Screenshot</h2>
              <img
                src={`http://127.0.0.1:8000/static/final.png?ts=${Date.now()}`}
                alt="screenshot"
                className="rounded border border-gray-700"
              />
            </div>

            {/* AI Explanation */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-lg col-span-2">
              <h2 className="text-lg mb-3">🧠 AI Explanation</h2>
              <p className="text-gray-300">
                {data.ai_explanation || "Generating explanation..."}
              </p>
            </div>

            {/* Test Cases */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-lg col-span-2">
              <h2 className="text-lg mb-3">🧪 Test Cases</h2>
              <div className="text-sm text-gray-300 whitespace-pre-wrap">
                {data.testcases || "Generating test cases..."}
              </div>
            </div>

          </div>
        )}
      </div>
    </div>
  );
}