import { Tag } from 'lucide-react';
import type { Finding } from '../types';
import { FindingCard } from './FindingCard';

interface CategorySectionProps {
  category: string;
  findings: Finding[];
}

export function CategorySection({ category, findings }: CategorySectionProps) {
  if (findings.length === 0) return null;

  const categoryName = category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());

  return (
    <div className="category-section">
      <div className="category-title">
        <Tag size={18} className="text-primary" style={{ color: 'var(--accent-main)' }} />
        {categoryName}
      </div>
      <div className="findings-list">
        {findings.map((finding, index) => (
          <FindingCard key={`${finding.id}-${index}`} finding={finding} />
        ))}
      </div>
    </div>
  );
}
