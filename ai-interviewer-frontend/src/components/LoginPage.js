import React from 'react';
import { Link } from 'react-router-dom';

const LoginPage = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
    <h1 className="text-3xl font-bold mb-6">Login Page</h1>
    <p className="mb-4">This is a placeholder for the login page.</p>
    <Link to="/" className="px-6 py-2 text-lg font-semibold text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors duration-300">
      Go to Home
    </Link>
  </div>
);

export default LoginPage; 