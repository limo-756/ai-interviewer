import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [submitError, setSubmitError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const validateEmail = (emailToValidate) => {
    if (!emailToValidate) {
      setEmailError('Email is required.');
      return false;
    }
    // Basic email format validation
    if (!/\S+@\S+\.\S+/.test(emailToValidate)) {
      setEmailError('Email address is invalid.');
      return false;
    }
    setEmailError('');
    return true;
  };

  const validatePassword = (passwordToValidate) => {
    if (!passwordToValidate) {
      setPasswordError('Password is required.');
      return false;
    }
    // Example: Password must be at least 6 characters
    // if (passwordToValidate.length < 6) {
    //   setPasswordError('Password must be at least 6 characters long.');
    //   return false;
    // }
    setPasswordError('');
    return true;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitError(''); // Clear previous submission errors
    setSuccessMessage(''); // Clear previous success messages

    const isEmailValid = validateEmail(email);
    const isPasswordValid = validatePassword(password);

    if (isEmailValid && isPasswordValid) {
      try {
        const response = await fetch('http://localhost:8000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
          // Handle successful login
          console.log('Login successful:', data);
          sessionStorage.setItem('access_token', data.access_token); // Save access token
          setSuccessMessage(data.message || 'Login successful!'); // Set success message
          // Navigate after a short delay to allow the user to see the message
          setTimeout(() => {
            navigate('/select-topic'); // Navigate to topic selection page
          }, 1500);
        } else {
          // Handle login failure
          setSubmitError(data.detail || 'Login failed. Please try again.');
          console.error('Login failed:', data);
        }
      } catch (error) {
        setSubmitError('An error occurred. Please try again later.');
        console.error('Login request error:', error);
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-700">Login</h1>
        {successMessage && <p className="text-green-500 text-sm mb-4 text-center">{successMessage}</p>}
        <form onSubmit={handleSubmit} noValidate>
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-gray-600 mb-1">Email Address</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (emailError) validateEmail(e.target.value); // Re-validate on change if there was an error
              }}
              onBlur={() => validateEmail(email)} // Validate on blur
              className={`w-full px-3 py-2 border ${emailError ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-2 ${emailError ? 'focus:ring-red-500' : 'focus:ring-blue-500'} focus:border-transparent`}
              required
              aria-describedby="email-error"
            />
            {emailError && <p id="email-error" className="text-red-500 text-xs mt-1">{emailError}</p>}
          </div>

          <div className="mb-6">
            <label htmlFor="password" className="block text-sm font-medium text-gray-600 mb-1">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                if (passwordError) validatePassword(e.target.value); // Re-validate on change if there was an error
              }}
              onBlur={() => validatePassword(password)} // Validate on blur
              className={`w-full px-3 py-2 border ${passwordError ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-2 ${passwordError ? 'focus:ring-red-500' : 'focus:ring-blue-500'} focus:border-transparent`}
              required
              aria-describedby="password-error"
            />
            {passwordError && <p id="password-error" className="text-red-500 text-xs mt-1">{passwordError}</p>}
          </div>

          {submitError && <p className="text-red-500 text-sm mb-4 text-center">{submitError}</p>}

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md shadow-md transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          >
            Login
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-gray-600">
          Don't have an account? <Link to="/signup" className="text-blue-500 hover:text-blue-700 font-medium">Sign up</Link>
        </p>
        <p className="mt-2 text-center text-sm text-gray-600">
          <Link to="/" className="text-blue-500 hover:text-blue-700 font-medium">Go to Home</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage; 