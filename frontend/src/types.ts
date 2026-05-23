export type Severity = 'info' | 'warning' | 'error';
export type Category = 'naming' | 'complexity' | 'best_practices' | 'maintainability' | 'syntax';

export interface Finding {
  id: string;
  title: string;
  category: Category;
  severity: Severity;
  line_number: number | null;
  line_numbers: number[];
  explanation: string;
  suggestion: string;
  example: string | null;
}

export interface AnalysisReport {
  score: number;
  summary: string;
  findings: Finding[];
}
