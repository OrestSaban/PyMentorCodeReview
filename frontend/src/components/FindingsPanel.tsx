import { useState, useMemo } from 'react';
import type { AnalysisReport, Finding, Severity } from '../types';
import { ScoreSummary } from './ScoreSummary';
import { CategorySection } from './CategorySection';
import { EmptyState } from './EmptyState';
import { FindingCard } from './FindingCard';
import { ToggleLeft, ToggleRight, AlertTriangle } from 'lucide-react';

interface FindingsPanelProps {
  report: AnalysisReport | null;
}

export function FindingsPanel({ report }: FindingsPanelProps) {
  const [filter, setFilter] = useState<Severity | 'all'>('all');
  const [compactMode, setCompactMode] = useState<boolean>(() => report ? report.findings.length > 8 : false);

  // Top Priorities must be defined before early return to satisfy React Rules of Hooks
  const topPriorities = useMemo(() => {
    if (!report || report.findings.length === 0) return [];
    const sorted = [...report.findings].sort((a, b) => {
      const sevWeight = { error: 3, warning: 2, info: 1 };
      if (sevWeight[a.severity] !== sevWeight[b.severity]) {
        return sevWeight[b.severity] - sevWeight[a.severity];
      }
      const catWeight = (c: string) => {
        if (c === 'syntax' || c === 'safety') return 4;
        if (c === 'complexity') return 3;
        if (c === 'best_practices') return 2;
        return 1;
      };
      return catWeight(b.category) - catWeight(a.category);
    });
    return sorted.slice(0, Math.min(4, sorted.length));
  }, [report]);

  if (!report) {
    return <EmptyState />;
  }

  const counts = {
    error: 0,
    warning: 0,
    info: 0
  };

  report.findings.forEach(f => {
    counts[f.severity]++;
  });

  const filteredFindings = filter === 'all' 
    ? report.findings 
    : report.findings.filter(f => f.severity === filter);

  // Group findings by category
  const findingsByCategory = filteredFindings.reduce((acc, finding) => {
    if (!acc[finding.category]) {
      acc[finding.category] = [];
    }
    acc[finding.category].push(finding);
    return acc;
  }, {} as Record<string, Finding[]>);

  const categories = Object.keys(findingsByCategory).sort();

  return (
    <div className="results-panel">
      <ScoreSummary report={report} />
      
      {report.findings.length === 0 ? (
        <div className="clean-state">
          <div style={{ fontSize: '3.5rem', lineHeight: 1 }}>🎉</div>
          <div>
            <h3>Nice work!</h3>
            <p>This looks clean for the current MVP checks. Remember: this tool checks selected beginner rules, not full program correctness.</p>
          </div>
        </div>
      ) : (
        <>
          <div className="findings-filters">
            <button 
              className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => setFilter('all')}
            >
              All ({report.findings.length})
            </button>
            <button 
              className={`filter-btn error ${filter === 'error' ? 'active' : ''}`}
              onClick={() => setFilter('error')}
            >
              Errors ({counts.error})
            </button>
            <button 
              className={`filter-btn warning ${filter === 'warning' ? 'active' : ''}`}
              onClick={() => setFilter('warning')}
            >
              Warnings ({counts.warning})
            </button>
            <button 
              className={`filter-btn info ${filter === 'info' ? 'active' : ''}`}
              onClick={() => setFilter('info')}
            >
              Info ({counts.info})
            </button>
            
            <div style={{ flex: 1 }} />
            <button 
              className="compact-toggle-btn" 
              onClick={() => setCompactMode(!compactMode)}
              title="Toggle Compact View"
            >
              {compactMode ? <ToggleLeft size={20} /> : <ToggleRight size={20} />}
              <span>{compactMode ? 'Compact' : 'Detailed'}</span>
            </button>
          </div>

          <div className="findings-container">
            {filter === 'all' && topPriorities.length > 0 && (
              <div className="top-priorities-section">
                <div className="top-priorities-header">
                  <AlertTriangle size={18} />
                  Top Priorities
                </div>
                <div className="top-priorities-list">
                  {topPriorities.map((finding, index) => (
                    <FindingCard key={`priority-${finding.id}-${index}`} finding={finding} compactMode={true} forceCollapsed={true} />
                  ))}
                </div>
              </div>
            )}
            
            {filteredFindings.length === 0 ? (
              <div className="empty-state" style={{ padding: '2rem 1rem' }}>
                <p style={{ color: 'var(--text-secondary)' }}>No {filter}s found in this code.</p>
              </div>
            ) : (
              categories.map((category) => (
                <CategorySection 
                  key={category} 
                  category={category} 
                  findings={findingsByCategory[category]} 
                  compactMode={compactMode}
                  allFindingsCount={report.findings.length}
                />
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}
