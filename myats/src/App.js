// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

function App() {
  const [jd, setJd] = useState('');
  const [resume, setResume] = useState(null);
  const [result, setResult] = useState('');

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    setResume(file);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('resume', resume);
    formData.append('jd', jd);
  
    try {
      const response = await axios.post('http://localhost:5000/evaluate', formData);
      setResult(response.data.result);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  const re=result;
  const formatResult = (text) => {
    const lines = text.split(/\d+\.\s+/).filter(Boolean);
  
    return (
      <div className="formatted-result">
        {lines.map((line, index) => (
          <div key={index} className="result-item">
            <div dangerouslySetInnerHTML={{ __html: line.replace(/\*\*(.*?)\*\*/g, (_, content) => `<strong>${content}</strong>`).replace(/(\d+)/g, '<span class="highlight">$1</span>') }} />
            {line.startsWith('*') && <br />} {/* Add line break if line starts with '*' */}
            <br />
          </div>
        ))}
      </div>
    );
  };
  
  
  return (
    <div className="container">
      <h1>Smart ATS</h1>
      <textarea
        placeholder="Paste job description here"
        value={jd}
        onChange={(e) => setJd(e.target.value)}
      />
      <button class="upload-button">
        <input type="file" accept=".pdf" onChange={handleFileUpload} />
      </button>
      <h4>only .pdf files</h4>
      <button onClick={handleSubmit}>Check Your Score</button>
      {<div>
  {formatResult(re)}
</div>}
    </div>
  );
}

export default App;
