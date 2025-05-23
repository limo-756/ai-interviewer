import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const TopicSelect = () => {
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [showResumePopup, setShowResumePopup] = useState(false);
  const [showCustomPopup, setShowCustomPopup] = useState(false);
  const [customTopic, setCustomTopic] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const topics = [
    'Computer networks',
    'Resume',
    'Product Management',
    'Custom',
  ];

  const handleTopicClick = (topic) => {
    setSelectedTopic(topic);
    setError('');
    if (topic === 'Resume') {
      setShowResumePopup(true);
    } else if (topic === 'Custom') {
      setShowCustomPopup(true);
    } else {
      startInterview(topic);
    }
  };

  const handleResumeUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
      setError('');
    } else {
      setResumeFile(null);
      setError('Please upload a PDF file.');
    }
  };

  const handleResumeSubmit = () => {
    if (selectedTopic === 'Resume' && !resumeFile) {
      setError('Please upload your resume to proceed.');
      return;
    }
    setShowResumePopup(false);
    startInterview(selectedTopic, resumeFile);
  };

  const handleCustomSubmit = () => {
    if (!customTopic.trim()) {
      setError('Please enter a custom topic.');
      return;
    }
    setShowCustomPopup(false);
    startInterview(customTopic);
  };

  const startInterview = async (topic, file = null) => {
    let requestBody = {
      topic: topic,
      resumeFile: "" // Default to empty string as Pydantic model expects a string
    };
    let resumeFileNameForLog = file ? file.name : 'N/A';

    if (file) {
      try {
        const fileContentBase64 = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(reader.result); // reader.result is the data URL (base64 encoded string)
          reader.onerror = (error) => reject(error);
          reader.readAsDataURL(file);
        });
        requestBody.resumeFile = fileContentBase64;
      } catch (err) {
        console.error('Error reading or encoding resume file:', err);
        setError('Failed to process the resume file. Please try again.');
        return; // Stop the process if file reading fails
      }
    }
    
    const token = sessionStorage.getItem('access_token'); // Get token from session storage
    console.log('Session value is :', token, " : ", typeof token);

    try {
      // Assuming your API endpoint is http://localhost:8000/start-interview
      const response = await fetch('http://localhost:8000/start-interview', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Set content type to JSON
          'access_token': token,
        },
        body: JSON.stringify(requestBody), // Send stringified JSON object
      });

      if (response.ok) {
        // Handle successful interview start, e.g., navigate to interview page
        // For now, let's assume it navigates to an /interview page
        const interviewData = await response.json();
        navigate('/interview', { state: { interviewData } }); 
        console.log('Interview started successfully for topic:', topic, 'with file:', resumeFileNameForLog);
      } else {
        // Try to parse JSON error, if it fails, provide a generic message
        const errorData = await response.json().catch(() => ({ detail: 'Failed to parse error response from server.' }));
        if (response.status === 400 && errorData.detail === "Session Expired") {
          navigate('/login', { state: { message: "Session Expired" } });
        } else {
          setError(errorData.detail || 'Failed to start interview. Please try again.'); // Use errorData.detail for FastAPI errors
        }
      }
    } catch (err) {
      console.error('Error starting interview:', err);
      setError('Failed to connect to the server. Please try again later.');
    }
  };
  
  const commonPopupStyle = {
    position: 'fixed',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)',
    zIndex: 1000,
    width: '350px',
    textAlign: 'center',
  };

  const backdropStyle = {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: 999,
  };

  const buttonStyle = {
    padding: '10px 20px',
    margin: '10px 5px 0',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '16px'
  };
  
  const primaryButtonStyle = { ...buttonStyle, backgroundColor: '#007bff', color: 'white'};
  const secondaryButtonStyle = { ...buttonStyle, backgroundColor: '#6c757d', color: 'white'};


  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px', fontFamily: 'Arial, sans-serif' }}>
      <h2 style={{ fontSize: '28px', marginBottom: '40px', color: '#333' }}>Choose a Topic for Your Interview</h2>
      {error && <p style={{ color: 'red', marginBottom: '20px', background: '#ffebee', border: '1px solid #ef9a9a', padding: '10px', borderRadius: '4px' }}>{error}</p>}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '30px', width: '100%', maxWidth: '600px' }}>
        {topics.map((topic) => (
          <button
            key={topic}
            onClick={() => handleTopicClick(topic)}
            style={{
              padding: '30px',
              fontSize: '18px',
              fontWeight: 'bold',
              color: 'white',
              backgroundColor: selectedTopic === topic ? '#0056b3' : '#007bff',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease, transform 0.2s ease',
              boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
              minHeight: '120px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              textAlign: 'center',
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#0056b3'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = selectedTopic === topic ? '#0056b3' : '#007bff'}
          >
            {topic}
          </button>
        ))}
      </div>

      {showResumePopup && (
        <>
          <div style={backdropStyle} onClick={() => setShowResumePopup(false)}></div>
          <div style={commonPopupStyle}>
            <h3 style={{marginTop: 0, marginBottom: '20px', color: '#333'}}>Upload Resume (PDF)</h3>
            <input type="file" accept=".pdf" onChange={handleResumeUpload} ref={fileInputRef} style={{display: 'block', margin: '0 auto 20px auto', padding: '10px', border: '1px solid #ddd', borderRadius: '4px', width: 'calc(100% - 22px)' }} />
            <button onClick={handleResumeSubmit} style={primaryButtonStyle}>Submit Resume</button>
            <button onClick={() => setShowResumePopup(false)} style={secondaryButtonStyle}>Cancel</button>
          </div>
        </>
      )}

      {showCustomPopup && (
        <>
          <div style={backdropStyle} onClick={() => setShowCustomPopup(false)}></div>
          <div style={commonPopupStyle}>
            <h3 style={{marginTop: 0, marginBottom: '20px', color: '#333'}}>Enter Custom Topic</h3>
            <input
              type="text"
              value={customTopic}
              onChange={(e) => setCustomTopic(e.target.value)}
              placeholder="e.g., System Design"
              style={{ width: 'calc(100% - 22px)', padding: '12px', marginBottom: '20px', border: '1px solid #ddd', borderRadius: '4px', boxSizing: 'border-box', fontSize: '16px' }}
            />
            <button onClick={handleCustomSubmit} style={primaryButtonStyle}>Start with this Topic</button>
            <button onClick={() => setShowCustomPopup(false)} style={secondaryButtonStyle}>Cancel</button>
          </div>
        </>
      )}
    </div>
  );
};

export default TopicSelect; 