import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setResult(null);
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/api/query', { query });
      setResult(response.data);
    } catch (err) {
      setError('An error occurred. Please check the server logs and try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderTable = (data) => {
    if (!data || data.length === 0 || data.error || data.message) {
        const message = data.error ? `SQL Error: ${data.error}` : (data.message || 'No SQL results found.');
        return <p>{message}</p>;
    }
    const headers = Object.keys(data[0]);
    return (
      <table>
        <thead>
          <tr>
            {headers.map(header => <th key={header}>{header}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {headers.map(header => <td key={header}>{String(row[header])}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const renderDocuments = (docs) => {
      if (!docs || docs.length === 0) {
          return <p>No relevant documents found.</p>;
      }
      return (
          <div className="doc-results">
              {docs.map((doc, index) => (
                  <div key={index} className="doc-card">
                      <h4>From: {doc.source}</h4>
                      <p>{doc.content}</p>
                  </div>
              ))}
          </div>
      );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>NLP Query Engine</h1>
        <form onSubmit={handleQuerySubmit}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your data..."
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Thinking...' : 'Ask'}
          </button>
        </form>

        {loading && <p>Loading...</p>}
        {error && <div className="error">{error}</div>}

        {result && (
          <div className="results">
            <h2>Document Results</h2>
            {renderDocuments(result.document_results)}

            <hr />

            <h2>Database Results</h2>
            <h3>Generated SQL</h3>
            <pre className="sql-query">{result.sql_results.generated_sql}</pre>
            <h3>Data</h3>
            {renderTable(result.sql_results.results)}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;