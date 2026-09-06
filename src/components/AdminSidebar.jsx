import { NavLink, useNavigate } from 'react-router-dom'

const ITEMS = [
  { to: '/admin/queue', label: 'Verification Queue', icon: '🗂️' },
  { to: '/admin/analytics', label: 'Analytics', icon: '📊' },
  { to: '/admin/archive', label: 'Reports Archive', icon: '🗃️' },
]

export default function AdminSidebar({ active }) {
  const navigate = useNavigate()
  return (
    <aside style={wrap}>
      <div>
        <div style={brandRow}>
          <div style={logoMark}>WT</div>
          <div>
            <div style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 15 }}>WeatherTrust</div>
            <div style={{ fontSize: 11, color: 'var(--text-on-navy-dim)' }}>Admin console</div>
          </div>
        </div>

        <nav style={{ marginTop: 28, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              style={({ isActive }) => ({
                ...linkStyle,
                background: isActive || active === item.to ? 'rgba(255,255,255,0.08)' : 'transparent',
                color: isActive || active === item.to ? '#fff' : 'var(--text-on-navy-dim)',
                borderLeft: isActive || active === item.to ? '3px solid var(--blue-accent)' : '3px solid transparent',
              })}
            >
              <span style={{ fontSize: 15 }}>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>

      <div>
        <div style={{ height: 1, background: 'rgba(255,255,255,0.08)', margin: '12px 0 16px' }} />
        <button
          onClick={() => navigate('/')}
          style={{ ...linkStyle, width: '100%', background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-on-navy-dim)' }}
        >
          <span style={{ fontSize: 15 }}>🌐</span> View public dashboard
        </button>
        <div style={userRow}>
          <div style={avatar}>R.K</div>
          <div>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#fff' }}>R. Kannan</div>
            <div style={{ fontSize: 11, color: 'var(--text-on-navy-dim)' }}>District Verifier</div>
          </div>
        </div>
      </div>
    </aside>
  )
}

const wrap = {
  width: 232,
  minHeight: '100vh',
  background: 'linear-gradient(180deg, var(--navy-950), var(--navy-900))',
  color: 'var(--text-on-navy)',
  padding: '20px 14px',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'space-between',
  position: 'sticky',
  top: 0,
  flexShrink: 0,
}
const brandRow = { display: 'flex', alignItems: 'center', gap: 10, padding: '0 8px' }
const logoMark = {
  width: 32, height: 32, borderRadius: 8,
  background: 'linear-gradient(135deg, var(--blue-accent), #6f9bff)',
  display: 'flex', alignItems: 'center', justifyContent: 'center',
  fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 12, color: '#fff',
}
const linkStyle = {
  display: 'flex', alignItems: 'center', gap: 10,
  padding: '10px 12px', borderRadius: 8, fontSize: 13.5, fontWeight: 500,
  textDecoration: 'none',
}
const userRow = { display: 'flex', alignItems: 'center', gap: 10, padding: '10px 8px 0' }
const avatar = {
  width: 30, height: 30, borderRadius: '50%', background: 'var(--navy-700)',
  display: 'flex', alignItems: 'center', justifyContent: 'center',
  fontSize: 11, fontWeight: 700, color: '#fff',
}
