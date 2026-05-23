export function EmptyState() {
  return (
    <div className="empty-state">
      <div className="empty-state-emoji">🦉</div>
      <h3>Ready to review</h3>
      <p>Paste a Python snippet and I'll review it like a friendly mentor.</p>
      
      <div className="example-checks">
        <div className="check-pill">✨ clear names</div>
        <div className="check-pill">🧩 simple functions</div>
        <div className="check-pill">🛡️ safe beginner patterns</div>
      </div>
    </div>
  );
}
