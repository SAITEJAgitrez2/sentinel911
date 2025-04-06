"use client";
import React from "react";

interface Props {
  result: any;
}

const ResultDisplay: React.FC<Props> = ({ result }) => {
  if (!result) return null;

  const { call_analysis, swat_check, dispatcher_report, explanation } = result;

  return (
    <div className="bg-blue-900 text-white p-6 rounded-lg mt-8 max-w-3xl mx-auto border border-blue-400 shadow-lg">
      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">📋 Analysis Result</h2>

      {/* Call Analysis */}
      <div className="mb-4">
        <h3 className="font-bold text-indigo-300">📞 Call Analysis</h3>
        <p><strong>Urgency Score:</strong> {call_analysis.urgency_score}</p>
        <p><strong>Deception Score:</strong> {call_analysis.deception_score}</p>
        <p><strong>Summary:</strong> {call_analysis.summary}</p>
        <p><strong>Duration:</strong> {call_analysis.duration} seconds</p>
        <p><strong>Status:</strong> {call_analysis.status}</p>
        <p><strong>Timestamp:</strong> {call_analysis.timestamp}</p>
      </div>

      {/* SWAT Check */}
      <div className="mb-4">
        <h3 className="font-bold text-red-300">🚨 SWAT Check</h3>
        <p><strong>Is SWAT:</strong> {swat_check.is_swat ? "Yes" : "No"}</p>
        {swat_check.is_swat && (
          <>
            <p><strong>Person Flagged:</strong> {swat_check.person_flagged}</p>
            <p><strong>Famous For:</strong> {swat_check.famous_for}</p>
            <p><strong>Reason:</strong> {swat_check.reason}</p>
          </>
        )}
      </div>

      {/* Dispatcher Report */}
      <div className="mb-4">
        <h3 className="font-bold text-yellow-300">🧑‍✈️ Dispatcher Report</h3>
        <p><strong>Dispatcher ID:</strong> {dispatcher_report.dispatcher_id}</p>
        <p><strong>Fatigue Score:</strong> {dispatcher_report.fatigue_score}</p>
        <p><strong>Neglect Flag:</strong> {dispatcher_report.neglect_flag ? "Yes" : "No"}</p>
        <p><strong>Anomaly Detected:</strong> {dispatcher_report.anomaly_detected ? "Yes" : "No"}</p>
        <p><strong>Total Calls:</strong> {dispatcher_report.details.total_calls}</p>
        <p><strong>Average Duration:</strong> {dispatcher_report.details.avg_duration}</p>
        <p><strong>Short Call Count:</strong> {dispatcher_report.details.short_call_count}</p>
        <p><strong>Drop Rate:</strong> {dispatcher_report.details.drop_rate}</p>
        <p><strong>Instant Alert:</strong> {dispatcher_report.details.instant_alert ? "Yes" : "No"}</p>
      </div>

      {/* Final Agent Explanation */}
      <div>
        <h3 className="font-bold text-pink-300">🤖 Agent Explanation</h3>
        <p className="italic mb-2">{explanation.summary}</p>
        <p>{explanation.explanation}</p>
      </div>
    </div>
  );
};

export default ResultDisplay;
