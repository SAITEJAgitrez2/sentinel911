import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import { ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

interface Alert {
  id: number;
  call_id: number;
  alert_type: string;
  severity: number;
  explanation: string;
  timestamp: string;
  is_resolved: boolean;
}

const Alerts: React.FC = () => {
  const { data: alerts, isLoading } = useQuery<Alert[]>('alerts', async () => {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/alerts`);
    return response.data;
  });

  const resolveAlert = async (alertId: number) => {
    await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/alerts/${alertId}/resolve`);
    // Invalidate and refetch
    // queryClient.invalidateQueries('alerts');
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Alerts</h1>

      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <ul className="divide-y divide-gray-200">
          {alerts?.map((alert) => (
            <li key={alert.id} className="p-6">
              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0">
                  {alert.is_resolved ? (
                    <CheckCircleIcon className="h-6 w-6 text-green-500" />
                  ) : (
                    <ExclamationTriangleIcon className="h-6 w-6 text-red-500" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {alert.alert_type.charAt(0).toUpperCase() + alert.alert_type.slice(1)} Alert
                      </p>
                      <p className="text-sm text-gray-500">
                        Call #{alert.call_id} • {new Date(alert.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <div className="flex items-center space-x-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        Severity: {(alert.severity * 100).toFixed(0)}%
                      </span>
                      {!alert.is_resolved && (
                        <button
                          onClick={() => resolveAlert(alert.id)}
                          className="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
                        >
                          Resolve
                        </button>
                      )}
                    </div>
                  </div>
                  <p className="mt-2 text-sm text-gray-500">{alert.explanation}</p>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Alerts; 