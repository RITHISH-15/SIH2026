import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import TopNav from '../components/TopNav'
import MapView from '../components/MapView'
import { EVENT_TYPES, CHENNAI_CENTER } from '../data/mockData'

const STEPS = ['Evidence', 'Location', 'Event', 'Details']

export default function ReportEvent() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [coords, setCoords] = useState(CHENNAI_CENTER)
  const [eventType, setEventType] = useState(null)
  const [description, setDescription] = useState('')
  const [submitted, setSubmitted] = useState(false)

  function handleFile(e) {
    const f = e.target.files?.[0]
    if (!f) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
  }

  function useMyLocation() {
    // Falls back to a Chennai-area default if geolocation is unavailable/denied.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => setCoords([pos.coords.latitude, pos.coords.longitude]),
        () => setCoords([13.0339 + (Math.random() - 0.5) * 0.04, 80.2496 + (Math.random() - 0.5) * 0.04])
      )
    }
  }

  function submit() {
    setSubmitted(true)
  }

  if (submitted) {
    return (
      <div>
        <TopNav />
        <div style={{ maxWidth: 560, margin: '80px auto', textAlign: 'center', padding: '0 24px' }}>
          <div style={{ fontSize: 44, marginBottom: 10 }}>✅</div>
          <h1 style={{ fontSize: 22, marginBottom: 8 }}>Your report is being verified</h1>
          <p style={{ fontSize: 14, color: 'var(--text-700)', lineHeight: 1.6 }}>
            Thanks — your submission was queued for automated metadata extraction, duplicate checks,
            and classification. Once the credibility engine scores it, it will appear on the public
            dashboard with a live verification status.
          </p>
          <div style={{ display: 'flex', gap: 10, justifyContent: 'center', marginTop: 24 }}>
            <button className="btn btn-primary" onClick={() => navigate('/')}>Go to dashboard</button>
            <button className="btn btn-ghost" onClick={() => { setSubmitted(false); setStep(0); setFile(null); setPreview(null); setEventType(null); setDescription('') }}>
              Submit another report
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div>
      <TopNav />
      <div style={{ maxWidth: 620, margin: '0 auto', padding: '30px 24px 60px' }}>
        <h1 style={{ fontSize: 22, marginBottom: 4 }}>Report a weather event</h1>
        <p style={{ fontSize: 13.5, color: 'var(--text-500)', marginBottom: 22 }}>
          Help verify real weather conditions across your neighborhood.
        </p>

        {/* stepper */}
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 26 }}>
          {STEPS.map((s, i) => (
            <div key={s} style={{ display: 'flex', alignItems: 'center', flex: i < STEPS.length - 1 ? 1 : 'unset' }}>
              <div style={{
                width: 26, height: 26, borderRadius: '50%', flexShrink: 0,
                display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 12, fontWeight: 700,
                background: i <= step ? 'var(--navy-700)' : 'var(--surface-sunken)',
                color: i <= step ? '#fff' : 'var(--text-500)',
              }}>
                {i < step ? '✓' : i + 1}
              </div>
              {i < STEPS.length - 1 && (
                <div style={{ flex: 1, height: 2, background: i < step ? 'var(--navy-700)' : 'var(--border)', margin: '0 6px' }} />
              )}
            </div>
          ))}
        </div>

        <div className="card" style={{ padding: 22 }}>
          {step === 0 && (
            <div>
              <h3 style={{ fontSize: 15, marginBottom: 12 }}>Visual evidence</h3>
              {!preview ? (
                <label style={dropzone}>
                  <input type="file" accept="image/*,video/*" onChange={handleFile} style={{ display: 'none' }} />
                  <div style={{ fontSize: 28 }}>📷</div>
                  <div style={{ fontSize: 13.5, fontWeight: 600, marginTop: 6 }}>Tap to capture or upload a photo/video</div>
                  <div style={{ fontSize: 12, color: 'var(--text-500)', marginTop: 4 }}>JPG, PNG or MP4 — under 50MB</div>
                </label>
              ) : (
                <div>
                  <img src={preview} alt="preview" style={{ width: '100%', maxHeight: 260, objectFit: 'cover', borderRadius: 10 }} />
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
                    <span style={{ fontSize: 12.5, color: 'var(--text-500)' }}>{file?.name}</span>
                    <button onClick={() => { setFile(null); setPreview(null) }} style={{ background: 'none', border: 'none', color: 'var(--blue-accent)', fontSize: 12.5, fontWeight: 600, cursor: 'pointer' }}>Change</button>
                  </div>
                </div>
              )}
            </div>
          )}

          {step === 1 && (
            <div>
              <h3 style={{ fontSize: 15, marginBottom: 12 }}>Location</h3>
              <MapView reports={[]} height={220} center={coords} zoom={14} />
              <button onClick={useMyLocation} className="btn btn-ghost" style={{ marginTop: 10 }}>📍 Use my current location</button>
              <div style={{ fontSize: 12, color: 'var(--text-500)', marginTop: 8 }}>
                GPS auto-fills from your browser. Fine-tune the pin by tapping a different point on the map if it's off.
              </div>
            </div>
          )}

          {step === 2 && (
            <div>
              <h3 style={{ fontSize: 15, marginBottom: 12 }}>Select event type</h3>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                {EVENT_TYPES.map((t) => (
                  <button
                    key={t.key}
                    onClick={() => setEventType(t.key)}
                    style={{
                      display: 'flex', alignItems: 'center', gap: 8, padding: '12px 14px', borderRadius: 10,
                      border: '1.5px solid', borderColor: eventType === t.key ? 'var(--blue-accent)' : 'var(--border)',
                      background: eventType === t.key ? 'rgba(47,111,237,0.06)' : '#fff',
                      cursor: 'pointer', fontSize: 13.5, fontWeight: 600, textAlign: 'left',
                    }}
                  >
                    <span style={{ fontSize: 18 }}>{t.icon}</span> {t.label}
                  </button>
                ))}
              </div>
              <div style={{ fontSize: 12, color: 'var(--text-500)', marginTop: 12 }}>
                This sets the initial category — our classifier may re-confirm or override it after submission.
              </div>
            </div>
          )}

          {step === 3 && (
            <div>
              <h3 style={{ fontSize: 15, marginBottom: 4 }}>Additional observations <span style={{ color: 'var(--text-500)', fontWeight: 400 }}>(optional)</span></h3>
              <textarea
                className="input"
                rows={5}
                placeholder="e.g. Water rising near the bus stop, knee deep, cars stalled..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                style={{ marginTop: 10, resize: 'vertical' }}
              />
              <div style={{ fontSize: 12, color: 'var(--text-500)', marginTop: 6 }}>{description.length}/280</div>
              <div style={{ marginTop: 14, padding: 12, borderRadius: 10, background: 'var(--teal-100)', color: 'var(--teal-600)', fontSize: 12.5 }}>
                🔒 Your report is secured by the WeatherTrust Data Protocol and cross-checked with IMD ground truth before publishing.
              </div>
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 22 }}>
            <button
              className="btn btn-ghost"
              onClick={() => setStep((s) => Math.max(0, s - 1))}
              style={{ visibility: step === 0 ? 'hidden' : 'visible' }}
            >
              Back
            </button>
            {step < STEPS.length - 1 ? (
              <button
                className="btn btn-primary"
                disabled={(step === 0 && !file) || (step === 2 && !eventType)}
                onClick={() => setStep((s) => s + 1)}
                style={{ opacity: (step === 0 && !file) || (step === 2 && !eventType) ? 0.5 : 1 }}
              >
                Continue
              </button>
            ) : (
              <button className="btn btn-accent" onClick={submit}>Submit verified report</button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

const dropzone = {
  display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
  padding: '36px 20px', border: '1.5px dashed var(--border-strong)', borderRadius: 12,
  cursor: 'pointer', textAlign: 'center',
}
