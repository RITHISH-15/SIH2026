import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import AdminSidebar from '../components/AdminSidebar'
import MapView from '../components/MapView'
import { reports } from '../data/mockData'

export default function RedZoneFactCheck() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [resolved, setResolved] = useState(false)
  const report = reports.find((r) => r.id === id) || reports.find((r) => r.factCheck)
  const fc = report?.factCheck

  return (
    <div style={{ display: 'flex' }}>
      <AdminSidebar />
      <div style={{ flex: 1, padding: '24px 28px', maxWidth: 1180 }}>
        <button onClick={() => navigate(-1)} style={{ background: 'none', border: 'none', color: 'var(--blue-accent)', fontSize: 13, fontWeight: 600, cursor: 'pointer', marginBottom: 10, padding: 0 }}>
          ← Back
        </button>

        <div style={{ background: 'var(--red-100)', color: 'var(--red-600)', padding: '10px 16px', borderRadius: 10, fontSize: 13, fontWeight: 600, marginBottom: 16 }}>
          🚩 Score {report?.score}/100 — routed to red-zone fact-check
        </div>

        <h1 style={{ fontSize: 20, marginBottom: 4 }}>Incident forensic fact-check comparison</h1>
        <div style={{ fontSize: 13, color: 'var(--text-500)', marginBottom: 20 }}>{report?.title} · {report?.area} · {report?.id}</div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 20 }}>
          <div className="card" style={{ padding: 18, borderColor: 'var(--red-600)' }}>
            <div style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--red-600)', marginBottom: 10 }}>CLAIM (AS SUBMITTED)</div>
            <img src={report?.thumb} alt="" style={{ width: '100%', height: 160, objectFit: 'cover', borderRadius: 8, marginBottom: 12 }} />
            <FactRow label="Reported rainfall" value={`${fc?.claim.rainfallMm} mm`} />
            <FactRow label="Reported wind" value={`${fc?.claim.windKmh} km/h`} />
            <p style={{ fontSize: 13, color: 'var(--text-700)', marginTop: 10, lineHeight: 1.5 }}>{fc?.claim.note}</p>
          </div>

          <div className="card" style={{ padding: 18 }}>
            <div style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)', marginBottom: 10 }}>VERIFIED GROUND TRUTH (IMD)</div>
            <MapView reports={[report]} height={160} center={[report?.lat, report?.lng]} zoom={12} />
            <div style={{ marginTop: 12 }}>
              <FactRow label="IMD-recorded rainfall" value={`${fc?.groundTruth.rainfallMm} mm`} />
              <FactRow label="IMD-recorded wind" value={`${fc?.groundTruth.windKmh} km/h`} />
            </div>
            <p style={{ fontSize: 13, color: 'var(--text-700)', marginTop: 10, lineHeight: 1.5 }}>{fc?.groundTruth.note}</p>
          </div>
        </div>

        <div className="card" style={{ padding: 18, marginBottom: 20 }}>
          <div style={{ fontSize: 13, fontWeight: 700, marginBottom: 6 }}>Nearby verified reports in this window</div>
          <div style={{ fontSize: 13, color: 'var(--text-500)' }}>
            {fc?.nearbyVerifiedCount === 0
              ? 'No other verified reports corroborate this claim within the radius and time window.'
              : `${fc?.nearbyVerifiedCount} nearby verified reports partially corroborate this claim.`}
          </div>
        </div>

        {!resolved ? (
          <div style={{ display: 'flex', gap: 10 }}>
            <button className="btn btn-danger-outline" onClick={() => setResolved('rejected')}>Still reject</button>
            <button className="btn btn-primary" onClick={() => setResolved('reconsidered')}>Reconsider — send to standard queue</button>
          </div>
        ) : (
          <div style={{ padding: 14, borderRadius: 10, background: resolved === 'rejected' ? 'var(--red-100)' : 'var(--amber-100)', color: resolved === 'rejected' ? 'var(--red-600)' : 'var(--amber-600)', fontSize: 13.5, fontWeight: 600 }}>
            {resolved === 'rejected'
              ? 'Finalized as hidden/rejected — logged for audit and model retraining.'
              : 'Sent back to the standard verification queue with this evidence attached.'}
          </div>
        )}
      </div>
    </div>
  )
}

function FactRow({ label, value }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '5px 0', fontSize: 13 }}>
      <span style={{ color: 'var(--text-500)' }}>{label}</span>
      <span style={{ fontWeight: 700 }}>{value}</span>
    </div>
  )
}
