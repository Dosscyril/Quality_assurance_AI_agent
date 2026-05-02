const runTest = async (goal = "explore") => {
  if (!url) {
    alert("Please enter a URL");
    return;
  }

  setLoading(true);
  setData(null);

  try {
    const response = await fetch("http://127.0.0.1:8000/run-agent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url.trim(),
        max_steps: 3,
        goal, // 🔥 IMPORTANT
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