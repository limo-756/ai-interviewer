import React from 'react';
import './App.css';
import SignUp from './components/SignUp';
import TopicSelect from './components/TopicSelect';
import InterviewPage from './components/InterviewPage';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import LoginPage from './components/LoginPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/select-topic" element={<TopicSelect />} />
          <Route path="/interview" element={<InterviewPage />} />
          {/* Define other routes here */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
