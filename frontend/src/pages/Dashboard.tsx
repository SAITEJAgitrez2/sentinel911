// src/pages/Dashboard.tsx
import React, { useState } from 'react';
import CallInput from '../components/CallInput';
import ResultCard from '../components/ResultCard';



const Dashboard: React.FC = () => {
  const [result, setResult] = useState<any>(null);

  return (
    <div className="min-h-screen bg-gray-100 p-6 space-y-6">
      <h1 className="text-3xl font-bold text-blue-900">🚨 Sentinel911 UI Dashboard</h1>
      <p className="text-gray-600">Welcome, Supervisor Chandra 💙</p>

      <CallInput onSubmit={setResult} />

      {result && <ResultCard data={result} />}
    </div>
  );
};

export default Dashboard;
