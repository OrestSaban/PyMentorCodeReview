import { Smile, Moon, Sun } from 'lucide-react';

interface AppHeaderProps {
  isDark: boolean;
  toggleTheme: () => void;
}

export function AppHeader({ isDark, toggleTheme }: AppHeaderProps) {
  return (
    <header className="header" style={{ position: 'relative' }}>
      <button 
        onClick={toggleTheme}
        style={{
          position: 'absolute',
          right: 0,
          top: '50%',
          transform: 'translateY(-50%)',
          background: 'var(--bg-surface)',
          border: '2px solid var(--border-light)',
          borderRadius: '50%',
          width: '44px',
          height: '44px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          color: 'var(--text-secondary)',
          boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
          transition: 'all 0.2s ease'
        }}
        title="Toggle dark mode"
      >
        {isDark ? <Sun size={20} /> : <Moon size={20} />}
      </button>
      
      <h1>
        <Smile size={32} className="text-primary" style={{ color: 'var(--accent-main)' }} />
        PyMentor Review
      </h1>
      <p>Friendly Python code review for beginners</p>
    </header>
  );
}
