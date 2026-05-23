import { useState } from 'react';
import { Tag, ChevronDown, ChevronUp } from 'lucide-react';
import type { Finding } from '../types';
import { FindingCard } from './FindingCard';

interface CategorySectionProps {
  category: string;
  findings: Finding[];
  compactMode?: boolean;
  allFindingsCount?: number;
}

export function CategorySection({ category, findings, compactMode = false, allFindingsCount = 0 }: CategorySectionProps) {
  const isImportant = category === 'syntax' || category === 'safety' || category === 'complexity';
  const shouldBeOpenDefault = isImportant || allFindingsCount <= 8;
  const [isOpen, setIsOpen] = useState(shouldBeOpenDefault);

  if (findings.length === 0) return null;

  const categoryName = category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());

  return (
    <div className="category-section">
      <div 
        className="category-title" 
        onClick={() => setIsOpen(!isOpen)}
        style={{ cursor: 'pointer', userSelect: 'none', display: 'flex', justifyContent: 'space-between' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Tag size={18} className="text-primary" style={{ color: 'var(--accent-main)' }} />
          {categoryName} <span className="category-count">({findings.length})</span>
        </div>
        {isOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
      </div>
      
      {isOpen && (
        <div className="findings-list">
          {findings.map((finding, index) => (
            <FindingCard 
              key={`${finding.id}-${index}`} 
              finding={finding} 
              compactMode={compactMode}
            />
          ))}
        </div>
      )}
    </div>
  );
}
