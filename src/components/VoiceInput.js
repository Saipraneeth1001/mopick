import React, { useState, useEffect } from 'react';
import './VoiceInput.css';

const VoiceInput = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if browser supports speech recognition
    if (!('webkitSpeechRecognition' in window)) {
      setError('Speech recognition is not supported in this browser.');
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = () => {
      setIsListening(true);
      setError('');
    };

    recognition.onresult = (event) => {
      const current = event.resultIndex;
      const transcript = event.results[current][0].transcript;
      setTranscript(transcript);
    };

    recognition.onerror = (event) => {
      setError(`Error occurred: ${event.error}`);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    return () => {
      recognition.stop();
    };
  }, []);

  const toggleListening = () => {
    if (isListening) {
      window.webkitSpeechRecognition.stop();
    } else {
      window.webkitSpeechRecognition.start();
    }
  };

  return (
    <div className="voice-input-container">
      <h1>Voice Input Demo</h1>
      <div className="voice-controls">
        <button 
          onClick={toggleListening}
          className={`voice-button ${isListening ? 'listening' : ''}`}
        >
          {isListening ? 'Stop Listening' : 'Start Listening'}
        </button>
      </div>
      {error && <div className="error-message">{error}</div>}
      <div className="transcript-container">
        <h2>Your Speech:</h2>
        <p>{transcript || 'Start speaking...'}</p>
      </div>
    </div>
  );
};

export default VoiceInput; 