import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';

interface DashboardStats {
  totalCalls: number;
  activeAlerts: number;
  averageUrgencyScore: number;
  totalDispatchers: number;
}

const Dashboard: React.FC = () => {
  const { data: stats, isLoading } = useQuery<DashboardStats>('dashboardStats', async () => {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/stats/dashboard`);
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
      <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Total Calls Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm font-medium text-gray-500">Total Calls</div>
          <div className="mt-2 text-3xl font-semibold text-gray-900">
            {stats?.totalCalls || 0}
          </div>
        </div>

        {/* Active Alerts Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm font-medium text-gray-500">Active Alerts</div>
          <div className="mt-2 text-3xl font-semibold text-red-600">
            {stats?.activeAlerts || 0}
          </div>
        </div>

        {/* Average Urgency Score Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm font-medium text-gray-500">Avg. Urgency Score</div>
          <div className="mt-2 text-3xl font-semibold text-indigo-600">
            {stats?.averageUrgencyScore?.toFixed(2) || '0.00'}
          </div>
        </div>

        {/* Total Dispatchers Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm font-medium text-gray-500">Total Dispatchers</div>
          <div className="mt-2 text-3xl font-semibold text-gray-900">
            {stats?.totalDispatchers || 0}
          </div>
        </div>
      </div>

      {/* Add more dashboard sections here */}
    </div>
  );
};

export default Dashboard; 