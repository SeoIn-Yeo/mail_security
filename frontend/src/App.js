import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [status, setStatus] = useState('Loading...');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await axios.get(`${API_URL}/health`);
        setStatus(response.data.status);
      } catch (error) {
        setStatus('Error connecting to API');
        console.error('API connection error:', error);
      }
    };
    checkHealth();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Mail Security</h1>
        <p>API Status: {status}</p>
      </header>
    </div>
  );
}

export default App;

