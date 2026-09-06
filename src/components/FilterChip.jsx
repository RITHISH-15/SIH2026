export default function FilterChip({ label, count, active, onClick, color }) {
  return (
    <button
      onClick={onClick}
      style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        width: '100%', padding: '8px 10px', borderRadius: 8, marginBottom: 4,
        border: '1px solid', borderColor: active ? 'var(--blue-accent)' : 'transparent',
        background: active ? 'rgba(47,111,237,0.08)' : 'transparent',
        cursor: 'pointer', fontSize: 13, fontWeight: active ? 600 : 500, color: 'var(--text-700)',
        textAlign: 'left',
      }}
    >
      <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        {color && <span style={{ width: 8, height: 8, borderRadius: '50%', background: color, flexShrink: 0 }} />}
        {label}
      </span>
      {count !== undefined && (
        <span style={{ fontSize: 11.5, color: 'var(--text-500)' }}>{count}</span>
      )}
    </button>
  )
}
