import React from 'react';
import { Link } from 'react-router-dom';
import { BellIcon, PhoneIcon, UserGroupIcon } from '@heroicons/react/24/outline';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <span className="text-xl font-bold text-indigo-600">Sentinel911</span>
            </Link>
          </div>
          
          <div className="flex space-x-8">
            <Link
              to="/calls"
              className="inline-flex items-center px-1 pt-1 text-gray-500 hover:text-gray-900"
            >
              <PhoneIcon className="h-6 w-6 mr-1" />
              Calls
            </Link>
            
            <Link
              to="/alerts"
              className="inline-flex items-center px-1 pt-1 text-gray-500 hover:text-gray-900"
            >
              <BellIcon className="h-6 w-6 mr-1" />
              Alerts
            </Link>
            
            <Link
              to="/dispatchers"
              className="inline-flex items-center px-1 pt-1 text-gray-500 hover:text-gray-900"
            >
              <UserGroupIcon className="h-6 w-6 mr-1" />
              Dispatchers
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 