import { useState, useEffect } from 'react';
import { AlertCircle } from 'lucide-react';
import type { AnalysisReport } from './types';

import { AppHeader } from './components/AppHeader';
import { CodeInputPanel } from './components/CodeInputPanel';
import { FindingsPanel } from './components/FindingsPanel';

function App() {
  const [code, setCode] = useState<string>('# Paste your Python code here...\n\ndef calculate_area(width, height):\n    return width * height\n');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<AnalysisReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDark, setIsDark] = useState(() => {
    const saved = localStorage.getItem('theme');
    return saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });

  useEffect(() => {
    if (isDark) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }, [isDark]);

  const toggleTheme = () => {
    const nextIsDark = !isDark;
    setIsDark(nextIsDark);
    if (nextIsDark) {
      document.body.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.body.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  const handleAnalyze = async () => {
    if (!code.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to analyze code. Make sure the backend is running.');
      }
      
      const data = await response.json();
      setReport(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <AppHeader isDark={isDark} toggleTheme={toggleTheme} />

      {error && (
        <div className="error-banner">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      <main className="main-content">
        <section className="input-section">
          <CodeInputPanel 
            code={code} 
            setCode={setCode} 
            onAnalyze={handleAnalyze} 
            loading={loading} 
          />
        </section>

        <section className="results-section">
          <FindingsPanel report={report} />
        </section>
      </main>
    </div>
  );
}

export default App;
