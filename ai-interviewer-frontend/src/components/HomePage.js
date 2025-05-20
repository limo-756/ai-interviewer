import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="relative min-h-screen bg-cover bg-center" style={{ backgroundImage: "url('https://source.unsplash.com/random/1920x1080?nature,water')" }}>
      <div className="absolute inset-0 bg-black opacity-50"></div>
      <div className="relative z-10 flex flex-col items-center justify-between min-h-screen p-4">
        <header className="w-full pt-8">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white text-center" style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)' }}>
            Welcome to Our Platform
          </h1>
        </header>

        <main className="flex-grow flex flex-col items-center justify-center">
          <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
            <Link to="/login">
              <button className="w-full sm:w-auto px-8 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-300">
                Login
              </button>
            </Link>
            <Link to="/signup">
              <button className="w-full sm:w-auto px-8 py-3 text-lg font-semibold text-white bg-green-600 rounded-lg shadow-md hover:bg-green-700 transition-colors duration-300">
                Sign up
              </button>
            </Link>
          </div>
        </main>

        <footer className="w-full pb-4 text-center">
          {/* Optional: Add footer content here */}
        </footer>
      </div>
    </div>
  );
};

export default HomePage; 