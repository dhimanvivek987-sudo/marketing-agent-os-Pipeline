import { useState } from "react";

function App() {
  const [companyUrl, setCompanyUrl] = useState("");
  const [status, setStatus] = useState("Waiting for input...");
  const [submittedUrl, setSubmittedUrl] = useState("");

  const handleRun = () => {
    if (!companyUrl.trim()) {
      setStatus("Please enter a company URL.");
      return;
    }

    setSubmittedUrl(companyUrl);
    setStatus("Frontend is ready. Backend connection is next.");
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f5f7fb",
        padding: "40px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          maxWidth: "900px",
          margin: "0 auto",
          background: "#ffffff",
          borderRadius: "16px",
          padding: "32px",
          boxShadow: "0 8px 24px rgba(0,0,0,0.08)",
        }}
      >
        <h1 style={{ marginBottom: "8px" }}>Marketing Agent OS</h1>
        <p style={{ marginTop: 0, color: "#555" }}>
          Multi-agent marketing and SDR workflow platform
        </p>

        <div style={{ marginTop: "30px" }}>
          <label
            htmlFor="companyUrl"
            style={{ display: "block", marginBottom: "10px", fontWeight: 600 }}
          >
            Enter Company URL
          </label>

          <input
            id="companyUrl"
            type="text"
            placeholder="https://company.com"
            value={companyUrl}
            onChange={(e) => setCompanyUrl(e.target.value)}
            style={{
              width: "100%",
              padding: "14px",
              borderRadius: "10px",
              border: "1px solid #ccc",
              fontSize: "16px",
              marginBottom: "16px",
            }}
          />

          <button
            onClick={handleRun}
            style={{
              padding: "12px 20px",
              borderRadius: "10px",
              border: "none",
              background: "#111827",
              color: "#fff",
              cursor: "pointer",
              fontSize: "15px",
            }}
          >
            Run Analysis
          </button>
        </div>

        <div
          style={{
            marginTop: "32px",
            padding: "20px",
            borderRadius: "12px",
            background: "#f9fafb",
            border: "1px solid #e5e7eb",
          }}
        >
          <h2 style={{ marginTop: 0 }}>Run Status</h2>
          <p>{status}</p>

          {submittedUrl && (
            <>
              <h3>Submitted URL</h3>
              <p>{submittedUrl}</p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;