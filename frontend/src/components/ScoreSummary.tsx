import type { AnalysisReport } from '../types';

interface ScoreSummaryProps {
  report: AnalysisReport;
}

export function ScoreSummary({ report }: ScoreSummaryProps) {
  const getScoreClass = (score: number) => {
    if (score >= 90) return 'excellent';
    if (score >= 70) return 'good';
    if (score >= 50) return 'fair';
    return 'poor';
  };

  return (
    <div className="score-summary">
      <div className={`score-circle ${getScoreClass(report.score)}`}>
        {report.score}
      </div>
      <div className="score-text">
        <h2>{report.score_label || report.summary}</h2>
        <p>Learning score</p>
      </div>
    </div>
  );
}
