export default function StatCard({ label, value, sub, accent = 'var(--navy-700)' }) {
  return (
    <div className="card" style={{ padding: '16px 18px', flex: 1, minWidth: 150 }}>
      <div style={{ fontSize: 12.5, color: 'var(--text-500)', fontWeight: 600 }}>{label}</div>
      <div style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 700, color: accent, marginTop: 6 }}>
        {value}
      </div>
      {sub && <div style={{ fontSize: 12, color: 'var(--text-500)', marginTop: 4 }}>{sub}</div>}
    </div>
  )
}
