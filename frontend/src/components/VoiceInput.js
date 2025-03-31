import React, { useState } from 'react';
import './VoiceInput.css';

const VoiceInput = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState('');
  const [recognition, setRecognition] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [movies, setMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

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
      searchMovies(finalTranscript); // Search movies when voice input is received
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

  const handleTextInputChange = (e) => {
    setTextInput(e.target.value);
  };

  

  const handleTextSubmit = (e) => {
    e.preventDefault();
    if (textInput.trim()) {
      searchMovies(textInput);
    }
  };

  const searchMovies = async (searchText) => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/movies/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: searchText
        })
      });
      const data = await response.json();
      setMovies(data.movies);
    } catch (err) {
      setError('Failed to fetch movies: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="voice-input-container">
      <h1>What do you wanna watch today?</h1>
      
      <div className="input-section">
        <form onSubmit={handleTextSubmit} className="text-input-form">
          <input
            type="text"
            value={textInput}
            onChange={handleTextInputChange}
            placeholder="Type your movie preference..."
            className="text-input"
          />
          <button type="submit" className="submit-button">Search</button>
        </form>

        <div className="voice-controls">
          <p>Or use voice input:</p>
          {!isListening ? (
            <button onClick={startListening} className="voice-button">
              Click to Speak
            </button>
          ) : (
            <button onClick={stopListening} className="voice-button listening">
              Finish
            </button>
          )}
        </div>
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

      {isLoading && <div className="loading">Loading movies...</div>}

      {movies.length > 0 && (
        <div className="movies-table-container">
          <table className="movies-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Year</th>
                <th>Rating</th>
                <th>Language</th>
                <th>Genre</th>
              </tr>
            </thead>
            <tbody>
              {movies.map((movie, index) => (
                <tr key={index}>
                  <td>{movie.title}</td>
                  <td>{movie.year}</td>
                  <td>{movie.rating}</td>
                  <td>{movie.language}</td>
                  <td>{movie.genre}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default VoiceInput; 