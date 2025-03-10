import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import ApplicationForm from './components/ApplicationForm';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="container py-5">
          <h1 className="mb-4">Job Application</h1>
          <ApplicationForm />
        </div>
      </header>
    </div>
  );
}

export default App;