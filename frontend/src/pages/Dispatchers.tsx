import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';

interface Dispatcher {
  id: number;
  name: string;
  badge_number: string;
  is_active: boolean;
  calls: {
    id: number;
    timestamp: string;
  }[];
}

const Dispatchers: React.FC = () => {
  const { data: dispatchers, isLoading } = useQuery<Dispatcher[]>('dispatchers', async () => {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/dispatchers`);
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
        <h1 className="text-3xl font-bold text-gray-900">Dispatchers</h1>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
          Add Dispatcher
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {dispatchers?.map((dispatcher) => (
          <div key={dispatcher.id} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">{dispatcher.name}</h3>
                  <p className="text-sm text-gray-500">Badge #{dispatcher.badge_number}</p>
                </div>
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    dispatcher.is_active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {dispatcher.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className="mt-4">
                <div className="text-sm text-gray-500">Recent Calls</div>
                <ul className="mt-2 divide-y divide-gray-200">
                  {dispatcher.calls.slice(0, 3).map((call) => (
                    <li key={call.id} className="py-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-900">Call #{call.id}</span>
                        <span className="text-sm text-gray-500">
                          {new Date(call.timestamp).toLocaleString()}
                        </span>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="bg-gray-50 px-4 py-4 sm:px-6">
              <button className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dispatchers; 