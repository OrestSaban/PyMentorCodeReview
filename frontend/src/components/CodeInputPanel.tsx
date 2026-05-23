import { Play } from 'lucide-react';
import { useRef } from 'react';

interface CodeInputPanelProps {
  code: string;
  setCode: (code: string) => void;
  onAnalyze: () => void;
  loading: boolean;
}

export function CodeInputPanel({ code, setCode, onAnalyze, loading }: CodeInputPanelProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null);

  const handleScroll = () => {
    if (textareaRef.current && lineNumbersRef.current) {
      lineNumbersRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  };

  const linesCount = Math.max(1, code.split('\n').length);
  const lineNumbers = Array.from({ length: linesCount }, (_, i) => i + 1);

  return (
    <div className="code-panel">
      <div className="code-wrapper">
        <div className="code-header">
          <span>📝 Python Code</span>
        </div>
        <div className="editor-layout">
          <div className="line-numbers" ref={lineNumbersRef}>
            {lineNumbers.map(n => <div key={n}>{n}</div>)}
          </div>
          <textarea
            ref={textareaRef}
            className="code-textarea"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onScroll={handleScroll}
            spellCheck={false}
            placeholder="# Paste your Python code here...&#10;&#10;def calculate_area(width, height):&#10;    return width * height"
          />
        </div>
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
