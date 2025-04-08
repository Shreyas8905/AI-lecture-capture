import React, { useRef, useState } from 'react';
import './App.css';

function App() {
  const [status, setStatus] = useState('');
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [filename, setFilename] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loadingTranscript, setLoadingTranscript] = useState(false);

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      await uploadFile(file);
    }
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      await uploadFile(file);
    }
  };

  const uploadFile = async (file) => {
    setStatus('Uploading...');
    setTranscript('');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const xhr = new XMLHttpRequest();
      xhr.open('POST', 'http://127.0.0.1:8000/upload');

      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
          const progress = Math.round((event.loaded / event.total) * 100);
          setUploadProgress(progress);
        }
      };

      xhr.onload = () => {
        if (xhr.status === 200) {
          const data = JSON.parse(xhr.responseText);
          setStatus({ message: `Success: ${data.message}`, type: 'success' });
          setFilename(data.filename);
        } else {
          setStatus({ message: 'Upload failed', type: 'error' });
        }
      };

      xhr.onerror = () => {
        setStatus({ message: 'Upload error', type: 'error' });
      };

      xhr.send(formData);
    } catch (error) {
      setStatus({ message: 'Upload error', type: 'error' });
      console.error(error);
    }
  };

  const handleGetTranscript = async () => {
    if (!filename) return;
    setLoadingTranscript(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/transcribe?filename=${encodeURIComponent(filename)}`);
      const data = await res.json();
      if (data.transcription) {
        setTranscript(data.transcription);
      } else {
        setTranscript('Transcription failed.');
      }
    } catch (error) {
      setTranscript('Transcription failed.');
      console.error(error);
    } finally {
      setLoadingTranscript(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  return (
    <main className="app-container">
      <section className="content-wrapper">
        <h1 className="app-title">📚 AI Lecture Capture</h1>
        <div
          className={`drop-zone ${isDragging ? 'dragging' : ''}`}
          onClick={() => fileInputRef.current.click()}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="upload-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 16V6m0 10 4-4m-4 4-4-4m9-8h-2.586a1 1 0 0 0-.707.293l-5.414 5.414a1 1 0 0 0 0 1.414l5.414 5.414a1 1 0 0 0 .707.293H21a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1Z" />
            </svg>
          </div>
          <p className="drop-zone-text">
            {isDragging ? 'Release to Upload' : 'Drag & drop your lecture video or click to browse'}
          </p>
        </div>

        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />

        <div className="progress-wrapper">
          {uploadProgress > 0 && (
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          )}
        </div>

        {filename && <p className="file-info">🎥 Uploaded: <strong>{filename}</strong></p>}

        <div className="status-bar">
          {status && (
            <div className={`status ${status.type}`}>{status.message}</div>
          )}
        </div>

        {filename && (
          <button className="transcribe-button" onClick={handleGetTranscript} disabled={loadingTranscript}>
            {loadingTranscript ? 'Transcribing...' : '✨ Get Transcript'}
          </button>
        )}
        {transcript && (
          <div className="transcript-box">
            <h2>📝 Transcription:</h2>
            <p>{transcript}</p>
          </div>
        )}
      </section>
    </main>
  );
}
export default App;
