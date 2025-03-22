import React, { useState } from 'react';
import './VoiceInput.css';

const VoiceInput = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState('');
  const [recognition, setRecognition] = useState(null);

  const startListening = () => {
    if (!('webkitSpeechRecognition' in window)) {
      setError('Speech recognition is not supported in this browser.');
      return;
    }

    const recognitionInstance = new window.webkitSpeechRecognition();
    recognitionInstance.continuous = true;
    recognitionInstance.interimResults = false; // We only want final results
    recognitionInstance.lang = 'en-US'; // Setting language to English

    recognitionInstance.onstart = () => {
      setIsListening(true);
      setError('');
      setTranscript(''); // Clear previous transcript
    };

    recognitionInstance.onresult = (event) => {
      const finalTranscript = Array.from(event.results)
        .map(result => result[0].transcript)
        .join(' ');
      setTranscript(finalTranscript);
    };

    recognitionInstance.onerror = (event) => {
      setError(`Error occurred: ${event.error}`);
      setIsListening(false);
    };

    setRecognition(recognitionInstance);
    recognitionInstance.start();
  };

  const stopListening = () => {
    if (recognition) {
      recognition.stop();
      setIsListening(false);
    }
  };

  return (
    <div className="voice-input-container">
      <h1>What do you wanna watch today?</h1>
      
      <div className="voice-controls">
        {!isListening ? (
          <button 
            onClick={startListening}
            className="voice-button"
          >
            Click to Speak
          </button>
        ) : (
          <button 
            onClick={stopListening}
            className="voice-button listening"
          >
            Finish
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}
      
      {transcript && (
        <div className="transcript-container">
          <h2>Your Speech:</h2>
          <p>{transcript}</p>
        </div>
      )}

      {isListening && (
        <div className="status-message">
          Listening....
        </div>
      )}
    </div>
  );
};

export default VoiceInput; 