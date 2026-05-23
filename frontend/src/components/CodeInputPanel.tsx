import { Play } from 'lucide-react';

interface CodeInputPanelProps {
  code: string;
  setCode: (code: string) => void;
  onAnalyze: () => void;
  loading: boolean;
}

export function CodeInputPanel({ code, setCode, onAnalyze, loading }: CodeInputPanelProps) {
  return (
    <div className="code-panel">
      <div className="code-wrapper">
        <div className="code-header">
          <span>📝 Python Code</span>
        </div>
        <textarea
          className="code-textarea"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          spellCheck={false}
          placeholder="# Paste your Python code here...&#10;&#10;def calculate_area(width, height):&#10;    return width * height"
        />
      </div>
      
      <div className="action-area">
        <button 
          className="btn-primary" 
          onClick={onAnalyze} 
          disabled={loading || !code.trim()}
        >
          {loading ? (
            <><Play size={20} className="spinner" /> Reviewing...</>
          ) : (
            <><Play size={20} /> Review my code</>
          )}
        </button>
        <div className="code-hint">
          Checks selected beginner-level rules.
        </div>
      </div>
    </div>
  );
}
