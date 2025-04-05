import React, { useState } from 'react';
import axios from 'axios';

interface AnalysisResult {
  urgencyScore: number;
  deceptionScore: number;
  summary: string;
}

interface DispatcherStatus {
  status: string;
  fatigueScore: number;
  recentCalls: number;
}

interface SwatResult {
  isSwat: boolean;
  confidence: number;
  reasoning: string;
}

export default function Dashboard() {
  const [transcript, setTranscript] = useState('');
  const [dispatcherId, setDispatcherId] = useState('');
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [dispatcherStatus, setDispatcherStatus] = useState<DispatcherStatus | null>(null);
  const [swatResult, setSwatResult] = useState<SwatResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Call Analysis
      const analysisRes = await axios.post('http://localhost:8000/api/analyze_call', {
        transcript
      });
      setAnalysis({
        urgencyScore: analysisRes.data.urgency_score,
        deceptionScore: analysisRes.data.deception_score,
        summary: analysisRes.data.summary
      });

      // Dispatcher Check
      const dispatcherRes = await axios.post('http://localhost:8000/api/check_dispatcher', {
        dispatcher_id: parseInt(dispatcherId)
      });
      setDispatcherStatus({
        status: dispatcherRes.data.status,
        fatigueScore: dispatcherRes.data.fatigue_score,
        recentCalls: dispatcherRes.data.recent_calls
      });

      // SWAT Detection
      const swatRes = await axios.post('http://localhost:8000/api/detect_swat', {
        call_data: transcript,
        dispatcher_id: parseInt(dispatcherId)
      });
      setSwatResult({
        isSwat: swatRes.data.is_swat,
        confidence: swatRes.data.confidence,
        reasoning: swatRes.data.reasoning
      });
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Sentinel911 Dashboard</h1>
      
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">
            Call Transcript
          </label>
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            className="w-full p-2 border rounded"
            rows={4}
          />
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">
            Dispatcher ID
          </label>
          <input
            type="text"
            value={dispatcherId}
            onChange={(e) => setDispatcherId(e.target.value)}
            className="w-full p-2 border rounded"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          {loading ? 'Analyzing...' : 'Analyze Call'}
        </button>
      </form>

      {analysis && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="p-4 border rounded">
            <h2 className="font-bold mb-2">Call Analysis</h2>
            <p>Urgency Score: {analysis.urgencyScore}</p>
            <p>Deception Score: {analysis.deceptionScore}</p>
            <p className="mt-2">{analysis.summary}</p>
          </div>

          {dispatcherStatus && (
            <div className="p-4 border rounded">
              <h2 className="font-bold mb-2">Dispatcher Status</h2>
              <p>Status: {dispatcherStatus.status}</p>
              <p>Fatigue Score: {dispatcherStatus.fatigueScore}</p>
              <p>Recent Calls: {dispatcherStatus.recentCalls}</p>
            </div>
          )}

          {swatResult && (
            <div className="p-4 border rounded">
              <h2 className="font-bold mb-2">SWAT Risk Assessment</h2>
              <p>SWAT Risk: {swatResult.isSwat ? 'High' : 'Low'}</p>
              <p>Confidence: {swatResult.confidence}</p>
              <p className="mt-2">{swatResult.reasoning}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
} 