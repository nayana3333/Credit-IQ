export function Badge({ status, tone, children }) {
  const styles = {
    approved: { bg: '#EEF6EE', text: '#15803D', border: '#BFE2C2', dot: '#1F9D45' },
    good: { bg: '#EEF6EE', text: '#15803D', border: '#BFE2C2', dot: '#1F9D45' },
    rejected: { bg: '#FBECEB', text: '#B91C1C', border: '#F3C6C3', dot: '#DC2626' },
    danger: { bg: '#FBECEB', text: '#B91C1C', border: '#F3C6C3', dot: '#DC2626' },
    pending: { bg: '#FDF3E6', text: '#B45309', border: '#F3DDB2', dot: '#D97706' },
    warning: { bg: '#FDF3E6', text: '#B45309', border: '#F3DDB2', dot: '#D97706' },
    info: { bg: '#EAF0FD', text: '#2554C7', border: '#C7D8F8', dot: '#2563EB' },
    neutral: { bg: '#FFFCF7', text: '#404040', border: '#E5E5E5', dot: '#A3A3A3' },
  };
  const key = String(status || tone || 'info').toLowerCase();
  const s = styles[key] || styles.neutral;
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, background: s.bg, color: s.text, border: `1px solid ${s.border}`, fontSize: 11, fontWeight: 600, padding: '2px 9px', borderRadius: 20, whiteSpace: 'nowrap' }}>
      <span style={{ width: 5, height: 5, borderRadius: '50%', background: s.dot, flexShrink: 0 }} />
      {children}
    </span>
  );
}

export default Badge;



