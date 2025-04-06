"use client";
import React, { useState } from "react";
import CallForm from "../components/CallForm";
import ResultDisplay from "../components/ResultDisplay";

export default function Home() {
  const [result, setResult] = useState(null);

  return (
    <main className="flex min-h-screen text-white font-sans">
      {/* Left Panel */}
      <div className="w-full md:w-1/2 bg-blue-950/95 backdrop-blur-md p-8 flex flex-col items-center justify-center space-y-6 relative z-10">
        {/* Logo */}
        <img src="/logo.png" alt="Sentinel911 Logo" className="w-50 h-50" />

        {/* Heading */}
        <h1 className="text-4xl font-extrabold text-center flex items-center justify-center">
          Call Analysis Dashboard
        </h1>

        {/* Form and Result */}
        <CallForm setResult={setResult} />
        {result && <ResultDisplay result={result} />}
      </div>

      {/* Right Panel */}
      <div className="hidden md:flex w-1/2 flex-col relative">
        {/* Background stack */}
        <div
          className="absolute inset-0 bg-cover bg-center opacity-90 z-0"
          style={{
            backgroundImage: `url('/ChatGPT_Image_Apr_6_2025_09_59_56_AM.png')`,
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        />
        {/* <div className="relative z-10 flex flex-col h-full justify-start pt-8 px-6 space-y-6 bg-black/40">
          <img src="/ambulance.png" alt="Ambulance" className="rounded shadow-lg w-80" />
          <img src="/fier.png" alt="Fire Rescue" className="rounded shadow-lg w-80" />
        </div> */}
      </div>
    </main>
  );
}
