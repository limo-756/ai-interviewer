import React from 'react';
import { Link } from 'react-router-dom';

const SignupPage = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
    <h1 className="text-3xl font-bold mb-6">Sign Up Page</h1>
    <p className="mb-4">This is a placeholder for the sign-up page.</p>
    <Link to="/" className="px-6 py-2 text-lg font-semibold text-white bg-green-500 rounded-lg hover:bg-green-600 transition-colors duration-300">
      Go to Home
    </Link>
  </div>
);

export default SignupPage; 