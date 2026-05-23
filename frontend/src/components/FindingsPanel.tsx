import type { AnalysisReport, Finding } from '../types';
import { ScoreSummary } from './ScoreSummary';
import { CategorySection } from './CategorySection';
import { EmptyState } from './EmptyState';

interface FindingsPanelProps {
  report: AnalysisReport | null;
}

export function FindingsPanel({ report }: FindingsPanelProps) {
  if (!report) {
    return <EmptyState />;
  }

  // Group findings by category
  const findingsByCategory = report.findings.reduce((acc, finding) => {
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
        <div className="findings-container">
          {categories.map((category) => (
            <CategorySection 
              key={category} 
              category={category} 
              findings={findingsByCategory[category]} 
            />
          ))}
        </div>
      )}
    </div>
  );
}
