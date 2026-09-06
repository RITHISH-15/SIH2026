import { NavLink, useNavigate } from 'react-router-dom'

const LINKS = [
  { to: '/', label: 'Home' },
  { to: '/report', label: 'Report an Event' },
  { to: '/about', label: 'About' },
]

export default function TopNav() {
  const navigate = useNavigate()
  return (
    <>
      <div style={bannerStyle}>
        <span>🛰️ Real-time citizen &amp; sensor weather-verification network for Tamil Nadu — Government of Tamil Nadu initiative</span>
        <NavLink to="/login" style={bannerLinkStyle}>Official IMD Chennai / TNSDMA partner login →</NavLink>
      </div>
      <header style={headerStyle}>
        <div style={brandWrap}>
          <div style={logoMark}>WT</div>
          <div>
            <div style={brandName}>WeatherTrust</div>
            <div style={brandSub}>Tamil Nadu</div>
          </div>
        </div>
        <nav style={navWrap}>
          {LINKS.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              style={({ isActive }) => ({
                ...navLinkStyle,
                color: isActive ? 'var(--navy-800)' : 'var(--text-500)',
                fontWeight: isActive ? 600 : 500,
              })}
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div style={{ display: 'flex', gap: 10 }}>
          <button className="btn btn-ghost" onClick={() => navigate('/login')}>Admin login</button>
          <button className="btn btn-accent" onClick={() => navigate('/report')}>Report Now</button>
        </div>
      </header>
    </>
  )
}

const bannerStyle = {
  background: 'var(--navy-900)',
  color: 'var(--text-on-navy)',
  fontSize: 12.5,
  padding: '7px 24px',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
}
const bannerLinkStyle = { color: '#bcd0ff', fontWeight: 600 }

const headerStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: '14px 24px',
  background: 'var(--surface)',
  borderBottom: '1px solid var(--border)',
  position: 'sticky',
  top: 0,
  zIndex: 20,
}
const brandWrap = { display: 'flex', alignItems: 'center', gap: 10 }
const logoMark = {
  width: 34, height: 34, borderRadius: 8,
  background: 'linear-gradient(135deg, var(--navy-700), var(--blue-accent))',
  color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center',
  fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 13,
}
const brandName = { fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 16.5, lineHeight: 1.1 }
const brandSub = { fontSize: 11, color: 'var(--text-500)' }
const navWrap = { display: 'flex', gap: 26 }
const navLinkStyle = { fontSize: 14 }
