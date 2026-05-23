import { Smile } from 'lucide-react';

export function AppHeader() {
  return (
    <header className="header">
      <h1>
        <Smile size={32} className="text-primary" style={{ color: 'var(--accent-main)' }} />
        PyMentor Review
      </h1>
      <p>Friendly Python code review for beginners</p>
    </header>
  );
}
