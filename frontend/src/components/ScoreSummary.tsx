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

  const getScoreMessage = (score: number) => {
    if (score >= 90) return 'Great job!';
    if (score >= 70) return 'Good start';
    if (score >= 50) return 'A few things to improve';
    return 'Let\'s fix a few things';
  };

  return (
    <div className="score-summary">
      <div className={`score-circle ${getScoreClass(report.score)}`}>
        {report.score}
      </div>
      <div className="score-text">
        <h2>{getScoreMessage(report.score)}</h2>
        <p>Learning score</p>
      </div>
    </div>
  );
}
