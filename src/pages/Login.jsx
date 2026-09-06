import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    if (!email || !password) {
      setError('Enter both your official email and password.')
      return
    }
    // Demo auth: any non-empty credentials issue a mock session and route in.
    setError('')
    navigate('/admin/queue')
  }

  return (
    <div style={wrap}>
      <div style={{ width: '100%', maxWidth: 380 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, justifyContent: 'center', marginBottom: 28 }}>
          <div style={logoMark}>WT</div>
          <div style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 18, color: '#fff' }}>WeatherTrust</div>
        </div>

        <div className="card" style={{ padding: 28, background: 'var(--surface)' }}>
          <h1 style={{ fontSize: 18, marginBottom: 4 }}>Admin &amp; verifier sign in</h1>
          <p style={{ fontSize: 12.5, color: 'var(--text-500)', marginBottom: 20 }}>
            Restricted to Tamil Nadu district verifiers and TNSDMA/IMD Chennai administrators. Public reporting needs no account.
          </p>

          <form onSubmit={handleSubmit}>
            <label className="field-label">Official email</label>
            <input className="input" type="email" placeholder="you@tnsdma.tn.gov.in" value={email} onChange={(e) => setEmail(e.target.value)} style={{ marginBottom: 14 }} />

            <label className="field-label">Password</label>
            <input className="input" type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} style={{ marginBottom: 8 }} />

            {error && <div style={{ fontSize: 12.5, color: 'var(--red-600)', marginBottom: 10 }}>{error}</div>}

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', margin: '10px 0 18px' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12.5, color: 'var(--text-500)' }}>
                <input type="checkbox" /> Keep me signed in
              </label>
              <a href="#" style={{ fontSize: 12.5, color: 'var(--blue-accent)', fontWeight: 600 }}>Forgot password?</a>
            </div>

            <button type="submit" className="btn btn-accent" style={{ width: '100%', justifyContent: 'center', padding: '11px 0' }}>
              Sign in
            </button>
          </form>
        </div>

        <div style={{ textAlign: 'center', marginTop: 16 }}>
          <a href="#/" style={{ fontSize: 12.5, color: 'var(--text-on-navy-dim)' }}>← Back to public dashboard</a>
        </div>
      </div>
    </div>
  )
}

const wrap = {
  minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
  background: 'linear-gradient(160deg, var(--navy-950), var(--navy-800))', padding: 24,
}
const logoMark = {
  width: 38, height: 38, borderRadius: 10,
  background: 'linear-gradient(135deg, var(--blue-accent), #6f9bff)',
  color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center',
  fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 14,
}
