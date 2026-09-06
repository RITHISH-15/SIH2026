import { useNavigate, useParams } from 'react-router-dom'
import TopNav from '../components/TopNav'
import StatusBadge from '../components/StatusBadge'
import MapView from '../components/MapView'
import { reports, nearbyFor, EVENT_TYPES, STATUS } from '../data/mockData'

export default function EventDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const report = reports.find((r) => r.id === id) || reports[0]
  const nearby = nearbyFor(report)
  const meta = EVENT_TYPES.find((t) => t.key === report.type)

  return (
    <div>
      <TopNav />
      <div style={{ maxWidth: 1120, margin: '0 auto', padding: '20px 24px 60px' }}>
        <button onClick={() => navigate(-1)} style={backBtn}>← Back to dashboard</button>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 20, marginTop: 10 }}>
          <div>
            <StatusBadge status={report.status} />
            <h1 style={{ fontSize: 24, marginTop: 10 }}>{meta?.icon} {report.title}</h1>
            <div style={{ fontSize: 13.5, color: 'var(--text-500)', marginTop: 4 }}>
              {report.area} · Reported {report.reportedAgo} · ID {report.id}
            </div>
          </div>
          {report.status === STATUS.FLAGGED && (
            <button className="btn btn-danger-outline" onClick={() => navigate(`/admin/redzone/${report.id}`)}>
              View red-zone fact-check
            </button>
          )}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: 20, marginTop: 20 }}>
          <div>
            <div className="card" style={{ overflow: 'hidden' }}>
              <img src={report.thumb} alt="" style={{ width: '100%', height: 300, objectFit: 'cover', display: 'block' }} />
              <div style={{ padding: 16 }}>
                <div style={{
                  padding: '10px 14px', borderRadius: 10, marginBottom: 14,
                  background: report.status === STATUS.VERIFIED ? 'var(--teal-100)' : report.status === STATUS.REVIEW ? 'var(--amber-100)' : 'var(--red-100)',
                  color: report.status === STATUS.VERIFIED ? 'var(--teal-600)' : report.status === STATUS.REVIEW ? 'var(--amber-600)' : 'var(--red-600)',
                  fontSize: 13.5, fontWeight: 600,
                }}>
                  {report.status === STATUS.VERIFIED && `Confirmed by ${report.sources} independent sources`}
                  {report.status === STATUS.REVIEW && `Awaiting confirmation — ${report.sources} source submitted so far`}
                  {report.status === STATUS.FLAGGED && 'Claim disputed against ground-truth reference data'}
                </div>
                <p style={{ fontSize: 14, color: 'var(--text-700)', lineHeight: 1.6 }}>{report.description}</p>
                <div style={{ fontSize: 12.5, color: 'var(--text-500)', marginTop: 10 }}>Submitted by {report.reporter}</div>
              </div>
            </div>

            <div style={{ marginTop: 18 }}>
              <h3 style={{ fontSize: 15, marginBottom: 8 }}>Location</h3>
              <MapView reports={[report, ...nearby]} height={260} center={[report.lat, report.lng]} zoom={12} />
            </div>
          </div>

          <div>
            <div className="card" style={{ padding: 16, marginBottom: 16 }}>
              <h3 style={{ fontSize: 14, marginBottom: 12 }}>Ground telemetry snapshot</h3>
              <TelemetryRow label="Rainfall" value={`${report.rainfallMm} mm`} />
              <TelemetryRow label="Wind speed" value={`${report.windKmh} km/h`} />
              <TelemetryRow label="Temperature" value={`${report.tempC} °C`} />
              <TelemetryRow label="Cross-source matches" value={report.sources} />
            </div>

            <div className="card" style={{ padding: 16 }}>
              <h3 style={{ fontSize: 14, marginBottom: 10 }}>Nearby related reports</h3>
              {nearby.length === 0 && <div style={{ fontSize: 13, color: 'var(--text-500)' }}>No related reports within this radius and window.</div>}
              {nearby.map((n) => (
                <button
                  key={n.id}
                  onClick={() => navigate(`/event/${n.id}`)}
                  style={{ display: 'flex', gap: 10, width: '100%', textAlign: 'left', padding: '8px 6px', border: 'none', borderTop: '1px solid var(--border)', background: 'none', cursor: 'pointer' }}
                >
                  <img src={n.thumb} alt="" style={{ width: 44, height: 44, borderRadius: 8, objectFit: 'cover' }} />
                  <div style={{ minWidth: 0 }}>
                    <div style={{ fontSize: 13, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{n.area}</div>
                    <div style={{ fontSize: 11.5, color: 'var(--text-500)' }}>{n.reportedAgo}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function TelemetryRow({ label, value }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '7px 0', borderBottom: '1px solid var(--border)', fontSize: 13.5 }}>
      <span style={{ color: 'var(--text-500)' }}>{label}</span>
      <span style={{ fontWeight: 600 }}>{value}</span>
    </div>
  )
}

const backBtn = { background: 'none', border: 'none', color: 'var(--blue-accent)', fontSize: 13.5, fontWeight: 600, cursor: 'pointer', padding: 0 }
