import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';

interface Call {
  id: number;
  transcript: string;
  audio_path: string;
  timestamp: string;
  duration: number;
  urgency_score: number;
  deception_score: number;
  dispatcher_id: number;
}

const Calls: React.FC = () => {
  const { data: calls, isLoading } = useQuery<Call[]>('calls', async () => {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/calls`);
    return response.data;
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">911 Calls</h1>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
          Upload Call
        </button>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {calls?.map((call) => (
            <li key={call.id} className="px-6 py-4 hover:bg-gray-50">
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-3">
                    <span className="text-sm font-medium text-gray-900">
                      Call #{call.id}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date(call.timestamp).toLocaleString()}
                    </span>
                  </div>
                  <div className="mt-1 text-sm text-gray-500 truncate">
                    {call.transcript.substring(0, 100)}...
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-sm text-gray-500">
                    Duration: {Math.round(call.duration)}s
                  </div>
                  <div className="text-sm">
                    <span className="text-indigo-600">
                      Urgency: {(call.urgency_score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <button className="text-indigo-600 hover:text-indigo-900">
                    View Details
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Calls; 