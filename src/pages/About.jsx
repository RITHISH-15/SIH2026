import TopNav from '../components/TopNav'

const STEPS = [
  { title: 'Citizen submits a report', body: 'A photo or video, GPS location, and event type are captured in under a minute from any phone.' },
  { title: 'Automated AI check', body: 'Metadata extraction, duplicate detection, and NLP classification run within seconds of submission.' },
  { title: 'Cross-check with IMD', body: 'The occurrence engine compares the claim against Doppler radar, AWS ground stations, and nearby reports.' },
  { title: 'Verified & published', body: 'Reports scoring above 70 go live instantly; borderline cases route to a human verifier before publishing.' },
]

const FAQS = [
  { q: 'How is the credibility score calculated?', a: 'It combines a source-reliability sub-score with a cross-source match sub-score computed against IMD telemetry and nearby citizen reports, producing a single 0–100 confidence figure.' },
  { q: 'Can I submit a report anonymously?', a: 'Yes — public reporting requires no account. Only district verifiers and administrators sign in, to keep the reporting flow frictionless for citizens.' },
  { q: 'What happens to rejected reports?', a: 'Nothing is silently deleted. Rejected and flagged submissions remain in the archive for audit and are used to retrain the classification model.' },
  { q: 'How fast does a report reach the public dashboard?', a: 'High-confidence reports (score above 70) can appear within a couple of minutes; borderline cases wait for a verifier decision, typically under two hours.' },
]

export default function About() {
  return (
    <div>
      <TopNav />
      <div style={{ maxWidth: 880, margin: '0 auto', padding: '40px 24px 70px' }}>
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          <h1 style={{ fontSize: 30, lineHeight: 1.2 }}>How WeatherTrust verifies reports</h1>
          <p style={{ fontSize: 15, color: 'var(--text-500)', maxWidth: 560, margin: '10px auto 0' }}>
            Every submission passes through the same scientific pipeline — a transparent process built
            with IMD Chennai's regional forecasting office, designed so nothing is a black box.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 14, marginBottom: 46 }}>
          {STEPS.map((s, i) => (
            <div key={s.title} className="card" style={{ padding: 18 }}>
              <div style={{ width: 30, height: 30, borderRadius: 8, background: 'var(--navy-700)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13, fontWeight: 700, marginBottom: 12 }}>
                {i + 1}
              </div>
              <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 6 }}>{s.title}</div>
              <div style={{ fontSize: 12.5, color: 'var(--text-500)', lineHeight: 1.5 }}>{s.body}</div>
            </div>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18, marginBottom: 46 }}>
          <div className="card" style={{ padding: 22 }}>
            <div style={{ fontSize: 22, marginBottom: 8 }}>👥</div>
            <h3 style={{ fontSize: 16, marginBottom: 6 }}>Crowdsourced ground truth</h3>
            <p style={{ fontSize: 13.5, color: 'var(--text-700)', lineHeight: 1.6 }}>
              Real people on real streets confirm conditions the moment they happen — the same signal
              emergency planners have always relied on, now structured and geotagged.
            </p>
          </div>
          <div className="card" style={{ padding: 22 }}>
            <div style={{ fontSize: 22, marginBottom: 8 }}>📡</div>
            <h3 style={{ fontSize: 16, marginBottom: 6 }}>Official sensor telemetry</h3>
            <p style={{ fontSize: 13.5, color: 'var(--text-700)', lineHeight: 1.6 }}>
              Doppler radar sweeps and automatic weather stations provide the independent reference
              every claim is checked against before it's called verified.
            </p>
          </div>
        </div>

        <h3 style={{ fontSize: 18, marginBottom: 16, textAlign: 'center' }}>Frequently asked questions</h3>
        <div>
          {FAQS.map((f) => (
            <details key={f.q} className="card" style={{ padding: '14px 18px', marginBottom: 10 }}>
              <summary style={{ fontSize: 14, fontWeight: 600, cursor: 'pointer' }}>{f.q}</summary>
              <p style={{ fontSize: 13.5, color: 'var(--text-700)', marginTop: 8, lineHeight: 1.6 }}>{f.a}</p>
            </details>
          ))}
        </div>

        <div style={{ marginTop: 46, padding: '28px 30px', borderRadius: 16, background: 'linear-gradient(120deg, var(--navy-800), var(--navy-950))', color: '#fff', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 20, flexWrap: 'wrap' }}>
          <div>
            <div style={{ fontSize: 18, fontWeight: 700, fontFamily: 'var(--font-display)' }}>Be the eyes on the ground in your city</div>
            <div style={{ fontSize: 13, color: 'var(--text-on-navy-dim)', marginTop: 4 }}>Every verified report helps district authorities respond faster.</div>
          </div>
          <div style={{ display: 'flex', gap: 10 }}>
            <a href="#/report" className="btn btn-accent">Submit a report</a>
            <a href="#/" className="btn btn-ghost" style={{ color: '#fff', borderColor: 'rgba(255,255,255,0.3)' }}>Explore the dashboard</a>
          </div>
        </div>
      </div>
    </div>
  )
}
