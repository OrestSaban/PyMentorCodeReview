import { useState } from 'react';
import { FileText, ChevronDown, ChevronUp, Info, ShieldAlert } from 'lucide-react';
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
  "empty-function": "This function is empty",
  "too-many-branches": "There are too many paths through this function",
  "complex-boolean-condition": "This condition is very complex",
  "unnecessary-else-after-return": "This 'else' block isn't needed",
  "range-len-loop": "Consider using direct iteration",
  "manual-counter-loop": "Use enumerate() instead of a manual counter",
  "unnecessary-list-conversion": "Unnecessary list() conversion",
  "repeated-condition": "Repeated condition in if/elif chain",
  "hardcoded-secret": "Hardcoded secret detected",
  "unsafe-yaml-load": "Unsafe YAML load detected",
  "subprocess-shell-true": "Subprocess shell=True detected",
  "assert-used-for-validation": "Avoid using assert for data validation",
  "large-top-level-script": "Too much logic outside of functions",
  "global-variable-modification": "Avoid changing global variables inside functions",
  "duplicate-string-literal": "Duplicate string literal",
  "todo-comment": "Review TODO comment"
};

interface FindingCardProps {
  finding: Finding;
  compactMode?: boolean;
  forceCollapsed?: boolean;
}

export function FindingCard({ finding, compactMode = false, forceCollapsed = false }: FindingCardProps) {
  const hasMultipleLines = finding.line_numbers && finding.line_numbers.length > 0;
  const title = FRIENDLY_TITLES[finding.id] || finding.title;
  
  const isImportant = finding.severity === 'error' || finding.category === 'syntax' || ['use-eval', 'exec-usage', 'subprocess-shell-true', 'hardcoded-secret', 'unsafe-yaml-load'].includes(finding.id);
  
  let shouldExpandDefault = !forceCollapsed && (isImportant || !compactMode);
  if (finding.severity === 'info') {
    shouldExpandDefault = false;
  }
  
  const [expanded, setExpanded] = useState(shouldExpandDefault);

  const occCount = finding.occurrences?.length || (hasMultipleLines ? finding.line_numbers!.length : (finding.line_number ? 1 : 0));

  return (
    <div className={`finding-card ${finding.severity} ${compactMode ? 'compact' : ''}`}>
      <div 
        className="finding-header" 
        onClick={() => setExpanded(!expanded)}
        style={{ cursor: 'pointer', userSelect: 'none' }}
      >
        <div className="finding-title-row">
          <div className="finding-title">
            {isImportant && <ShieldAlert size={16} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'text-bottom' }} />}
            {title}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <SeverityBadge severity={finding.severity} />
            {expanded ? <ChevronUp size={20} className="text-secondary" /> : <ChevronDown size={20} className="text-secondary" />}
          </div>
        </div>
        
        {!expanded && (
          <div className="finding-collapsed-preview">
            <div className="finding-preview-meta">
              <span className="finding-id-badge">{finding.id}</span>
              {occCount > 0 && (
                <span className="finding-occ-badge">
                  <FileText size={12} /> {occCount} {occCount === 1 ? 'place' : 'places'}
                </span>
              )}
            </div>
            <div className="finding-preview-suggestion">
              <Info size={14} /> {finding.suggestion}
            </div>
          </div>
        )}
      </div>
      
      {expanded && (
        <div className="finding-expanded-content">
          <div className="finding-snippets-section">
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
      )}
    </div>
  );
}
