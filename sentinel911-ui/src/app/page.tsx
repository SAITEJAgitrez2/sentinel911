"use client";
import React, { useState } from "react";
import CallForm from "../components/CallForm";
import ResultDisplay from "../components/ResultDisplay";

export default function Home() {
  const [result, setResult] = useState(null);

  return (
    <main className="min-h-screen bg-gradient-to-r from-blue-900 to-black text-white p-8">
      <h1 className="text-4xl font-extrabold text-center mb-10 flex items-center justify-center">
        <span className="mr-3">🚓</span> Sentinel911 Call Analysis Dashboard
      </h1>

      <CallForm setResult={setResult} />
      {result && <ResultDisplay result={result} />}
    </main>
  );
}
