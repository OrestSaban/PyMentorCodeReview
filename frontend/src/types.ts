export type Severity = 'info' | 'warning' | 'error';
export type Category = 'naming' | 'complexity' | 'best_practices' | 'maintainability' | 'syntax';

export interface Occurrence {
  line: number;
  col: number | null;
  snippet: string;
  value: string | null;
}

export interface Finding {
  id: string;
  title: string;
  category: Category;
  severity: Severity;
  line_number: number | null;
  line_numbers: number[];
  col: number | null;
  snippet: string | null;
  occurrences: Occurrence[];
  explanation: string;
  suggestion: string;
  example: string | null;
}

export interface AnalysisReport {
  score: number;
  score_label: string;
  summary: string;
  findings: Finding[];
}
