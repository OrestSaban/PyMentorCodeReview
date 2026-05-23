import { AlertCircle, AlertTriangle, Info } from 'lucide-react';
import type { Severity } from '../types';

export function SeverityBadge({ severity }: { severity: Severity }) {
  const getIcon = () => {
    switch (severity) {
      case 'error': return <AlertCircle size={14} />;
      case 'warning': return <AlertTriangle size={14} />;
      case 'info': return <Info size={14} />;
      default: return null;
    }
  };

  return (
    <span className={`severity-badge ${severity}`}>
      {getIcon()}
      {severity}
    </span>
  );
}
