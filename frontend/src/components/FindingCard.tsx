import { FileText } from 'lucide-react';
import type { Finding } from '../types';
import { SeverityBadge } from './SeverityBadge';

const FRIENDLY_TITLES: Record<string, string> = {
  "unclear-variable-name": "This name could be clearer",
  "non-snake-case-function": "Function names are usually snake_case",
  "function-too-long": "This function is getting a bit complex",
  "too-many-parameters": "A lot of parameters here",
  "nested-if-too-deep": "This logic is getting deeply nested",
  "print-in-function": "Consider returning instead of printing",
  "compare-boolean": "No need to compare with True/False",
  "bare-except": "Careful with bare except blocks",
  "use-eval": "Careful with eval()",
  "magic-number": "This value may need a name",
  "syntax-error": "Oops, there's a syntax error",
  "mutable-default-argument": "Watch out for mutable defaults",
  "exec-usage": "Executing dynamic code is risky",
  "broad-exception": "This except block is too broad",
  "missing-return-value": "Did you forget to return?",
  "non-snake-case-variable": "Variable names are usually snake_case",
  "constant-not-uppercase": "Constants should be UPPERCASE",
  "shadowing-builtin-name": "This name hides a built-in Python function",
  "unclear-function-name": "This function name is too generic",
  "inconsistent-return": "This function might accidentally return None",
  "too-many-local-variables": "Too many local variables",
  "empty-function": "This function is empty"
};

export function FindingCard({ finding }: { finding: Finding }) {
  const hasMultipleLines = finding.line_numbers && finding.line_numbers.length > 0;
  const title = FRIENDLY_TITLES[finding.id] || finding.title;
  
  return (
    <div className={`finding-card ${finding.severity}`}>
      <div className="finding-header">
        <div className="finding-title-row">
          <div className="finding-title">{title}</div>
          <SeverityBadge severity={finding.severity} />
        </div>
        
        {finding.occurrences && finding.occurrences.length > 0 ? (
          <div className="finding-snippets-container">
            {finding.occurrences.map((occ, idx) => (
              <div key={idx} className="finding-snippet-row">
                <div className="finding-lines">
                  <FileText size={14} />
                  Line {occ.line}{occ.col !== null ? `:${occ.col}` : ''}
                  {occ.value && <span className="finding-value-badge">({occ.value})</span>}
                </div>
                {occ.snippet && <div className="finding-snippet-code">{occ.snippet}</div>}
              </div>
            ))}
          </div>
        ) : (finding.line_number || hasMultipleLines) ? (
          <div className="finding-snippet-row">
            <div className="finding-lines">
              <FileText size={14} />
              {hasMultipleLines 
                ? `Lines ${finding.line_numbers.join(', ')}`
                : `Line ${finding.line_number}${finding.col !== null ? `:${finding.col}` : ''}`}
            </div>
            {finding.snippet && <div className="finding-snippet-code">{finding.snippet}</div>}
          </div>
        ) : null}
      </div>
      
      <div className="finding-section">
        <div className="finding-label">Why it matters</div>
        <div className="finding-explanation">{finding.explanation}</div>
      </div>
      
      <div className="finding-section">
        <div className="finding-label">Try this</div>
        <div className="finding-suggestion">{finding.suggestion}</div>
      </div>
      
      {finding.example && (
        <div className="finding-example">
          {finding.example}
        </div>
      )}
    </div>
  );
}
