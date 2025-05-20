import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you are using react-router-dom for navigation

const HomePage = () => {
  return (
    <div
      className="min-h-screen bg-cover bg-center flex flex-col items-center justify-between p-8"
      style={{ backgroundImage: "url('https://images.unsplash.com/photo-1506744038136-46273834b3fb')" }}
    >
      {/* Semi-transparent overlay */}
      <div className="absolute inset-0 bg-black opacity-50"></div>

      {/* Title */}
      <div className="relative z-10 text-center mt-16 md:mt-24">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-white" style={{ textShadow: '2px 2px 4px rgba(0,0,0,0.5)' }}>
          Welcome to Our Platform
        </h1>
      </div>

      {/* Centered Buttons */}
      <div className="relative z-10 flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-16 md:mb-24">
        <Link to="/login">
          <button className="w-48 sm:w-auto bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg text-lg shadow-md hover:shadow-xl transition duration-300 ease-in-out transform hover:-translate-y-1">
            Login
          </button>
        </Link>
        <Link to="/signup">
          <button className="w-48 sm:w-auto bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-lg text-lg shadow-md hover:shadow-xl transition duration-300 ease-in-out transform hover:-translate-y-1">
            Sign up
          </button>
        </Link>
      </div>

      {/* Empty div to push buttons to center if content is less, or adjust justify-between on main div for more control*/}
      <div></div>

    </div>
  );
};

export default HomePage; 