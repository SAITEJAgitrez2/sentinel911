"use client";
import React, { useState } from "react";

interface Props {
  setResult: (result: any) => void;
}

const CallForm: React.FC<Props> = ({ setResult }) => {
  const [dispatcherId, setDispatcherId] = useState("");
  const [callerAddress, setCallerAddress] = useState("");
  const [callerId, setCallerId] = useState("Unknown");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!dispatcherId || !file) {
      alert("Dispatcher ID and file are required!");
      return;
    }
  
    const formData = new FormData();
    formData.append("dispatcher_id", dispatcherId);
    formData.append("caller_address", callerAddress);
    formData.append("caller_id", callerId);
    formData.append("file", file);
  
    try {
      setLoading(true);
      setError(null);
  
      const response = await fetch("http://127.0.0.1:8000/api/agent/full_analysis", {
        method: "POST",
        body: formData,
      });
  
      const contentType = response.headers.get("content-type");
  
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${errorText}`);
      }
  
      if (contentType?.includes("application/json")) {
        const data = await response.json();
        setResult(data);
      } else {
        const text = await response.text();
        throw new Error(`Expected JSON but got: ${text}`);
      }
  
    } catch (err: any) {
      console.error("Submission Error:", err);
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="bg-blue-950 p-6 rounded-lg shadow-lg max-w-2xl mx-auto space-y-4 border border-blue-300">
      <input
        type="text"
        placeholder="Dispatcher ID"
        className="w-full p-2 rounded bg-blue-900 border border-blue-500 text-white"
        value={dispatcherId}
        onChange={(e) => setDispatcherId(e.target.value)}
      />
      <input
        type="text"
        placeholder="Caller Address"
        className="w-full p-2 rounded bg-blue-900 border border-blue-500 text-white"
        value={callerAddress}
        onChange={(e) => setCallerAddress(e.target.value)}
      />
      <input
        type="text"
        placeholder="Caller ID (optional)"
        className="w-full p-2 rounded bg-blue-900 border border-blue-500 text-white"
        value={callerId}
        onChange={(e) => setCallerId(e.target.value)}
      />
      <input
        type="file"
        accept=".wav"
        className="w-full p-2 bg-blue-900 text-white file:bg-blue-700 file:text-white file:border-0 file:rounded"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button
        onClick={handleSubmit}
        className="w-full bg-indigo-600 hover:bg-indigo-500 transition font-bold py-2 rounded text-white"
        disabled={loading}
      >
        {loading ? "Submitting..." : "Submit Call"}
      </button>
      {error && <p className="text-red-400 text-sm text-center">{error}</p>}
    </div>
  );
};

export default CallForm;
