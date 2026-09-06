import { useState } from 'react'
import AdminSidebar from '../components/AdminSidebar'
import StatCard from '../components/StatCard'
import { reports, STATUS, EVENT_TYPES } from '../data/mockData'

export default function VerificationQueue() {
  const [queue, setQueue] = useState(reports.filter((r) => r.status === STATUS.REVIEW))
  const [selected, setSelected] = useState(null)

  function decide(id, decision) {
    setQueue((q) => q.filter((r) => r.id !== id))
    setSelected(null)
    // decision === 'approve' | 'reject' — in a real backend this would PATCH
    // the report's status and move it into the Verified Event Store / audit log.
    console.log(`Report ${id} -> ${decision}`)
  }

  return (
    <div style={{ display: 'flex' }}>
      <AdminSidebar active="/admin/queue" />
      <div style={{ flex: 1, padding: '24px 28px', maxWidth: 1180 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 18 }}>
          <div>
            <h1 style={{ fontSize: 21 }}>Verification queue</h1>
            <div style={{ fontSize: 13, color: 'var(--text-500)' }}>
              Reports scoring 41–70 — the only zone that needs a human decision.
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
          <StatCard label="Pending cases" value={queue.length} accent="var(--amber-600)" />
          <StatCard label="High priority" value={queue.filter((r) => r.score < 55).length} sub="Score under 55" />
          <StatCard label="Avg. resolution" value="1.8 min" />
        </div>

        <div className="card">
          <div style={{ display: 'grid', gridTemplateColumns: '2.4fr 1fr 1.3fr 0.9fr', padding: '10px 18px', fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)', borderBottom: '1px solid var(--border)' }}>
            <div>REPORT</div>
            <div>EVENT TYPE</div>
            <div>CREDIBILITY SCORE</div>
            <div>ACTIONS</div>
          </div>
          {queue.length === 0 && (
            <div style={{ padding: 30, textAlign: 'center', fontSize: 13.5, color: 'var(--text-500)' }}>
              Queue clear — no reports currently need human review.
            </div>
          )}
          {queue.map((r) => {
            const meta = EVENT_TYPES.find((t) => t.key === r.type)
            return (
              <div
                key={r.id}
                onClick={() => setSelected(r)}
                style={{ display: 'grid', gridTemplateColumns: '2.4fr 1fr 1.3fr 0.9fr', alignItems: 'center', padding: '12px 18px', borderBottom: '1px solid var(--border)', cursor: 'pointer' }}
              >
                <div style={{ display: 'flex', gap: 10, alignItems: 'center', minWidth: 0 }}>
                  <img src={r.thumb} alt="" style={{ width: 40, height: 40, borderRadius: 8, objectFit: 'cover', flexShrink: 0 }} />
                  <div style={{ minWidth: 0 }}>
                    <div style={{ fontSize: 13.5, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{r.title}</div>
                    <div style={{ fontSize: 12, color: 'var(--text-500)' }}>{r.area} · {r.reportedAgo}</div>
                  </div>
                </div>
                <div style={{ fontSize: 13 }}>{meta?.icon} {meta?.label}</div>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <div style={{ flex: 1, height: 6, borderRadius: 3, background: 'var(--surface-sunken)' }}>
                      <div style={{ width: `${r.score}%`, height: '100%', borderRadius: 3, background: 'var(--amber-600)' }} />
                    </div>
                    <span style={{ fontSize: 12.5, fontWeight: 700 }}>{r.score}</span>
                  </div>
                </div>
                <div style={{ display: 'flex', gap: 6 }} onClick={(e) => e.stopPropagation()}>
                  <button className="btn btn-primary" style={{ padding: '6px 10px', fontSize: 12 }} onClick={() => decide(r.id, 'approve')}>Approve</button>
                  <button className="btn btn-danger-outline" style={{ padding: '6px 10px', fontSize: 12 }} onClick={() => decide(r.id, 'reject')}>Reject</button>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {selected && (
        <div style={overlay} onClick={() => setSelected(null)}>
          <div style={drawer} onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 14 }}>
              <div>
                <div style={{ fontSize: 12, color: 'var(--text-500)' }}>{selected.id}</div>
                <h2 style={{ fontSize: 18 }}>{selected.title}</h2>
                <div style={{ fontSize: 13, color: 'var(--text-500)' }}>{selected.area}</div>
              </div>
              <button onClick={() => setSelected(null)} style={{ background: 'none', border: 'none', fontSize: 18, cursor: 'pointer' }}>✕</button>
            </div>

            <img src={selected.thumb} alt="" style={{ width: '100%', height: 200, objectFit: 'cover', borderRadius: 10, marginBottom: 14 }} />

            <div style={{ marginBottom: 14 }}>
              <div style={{ fontSize: 12.5, fontWeight: 700, marginBottom: 6 }}>Score breakdown</div>
              <ScoreBar label="Source reliability" value={Math.round(selected.score * 0.55)} />
              <ScoreBar label="Cross-source match" value={Math.round(selected.score * 0.45)} />
              <div style={{ fontSize: 12.5, color: 'var(--text-500)', marginTop: 6 }}>Combined score: {selected.score} / 100</div>
            </div>

            <div style={{ marginBottom: 18 }}>
              <div style={{ fontSize: 12.5, fontWeight: 700, marginBottom: 6 }}>GPS &amp; metadata</div>
              <div style={{ fontSize: 13, color: 'var(--text-700)' }}>
                {selected.lat.toFixed(4)}, {selected.lng.toFixed(4)} · {selected.rainfallMm}mm rainfall · {selected.windKmh}km/h wind
              </div>
            </div>

            <div style={{ display: 'flex', gap: 10 }}>
              <button className="btn btn-primary" style={{ flex: 1, justifyContent: 'center' }} onClick={() => decide(selected.id, 'approve')}>Approve</button>
              <button className="btn btn-danger-outline" style={{ flex: 1, justifyContent: 'center' }} onClick={() => decide(selected.id, 'reject')}>Reject</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function ScoreBar({ label, value }) {
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 3 }}>
        <span style={{ color: 'var(--text-500)' }}>{label}</span>
        <span style={{ fontWeight: 600 }}>{value}</span>
      </div>
      <div style={{ height: 6, borderRadius: 3, background: 'var(--surface-sunken)' }}>
        <div style={{ width: `${value}%`, height: '100%', borderRadius: 3, background: 'var(--navy-700)' }} />
      </div>
    </div>
  )
}

const overlay = {
  position: 'fixed', inset: 0, background: 'rgba(10,24,48,0.35)',
  display: 'flex', justifyContent: 'flex-end', zIndex: 50,
}
const drawer = {
  width: 400, background: '#fff', height: '100vh', overflowY: 'auto',
  padding: 22, boxShadow: 'var(--shadow-pop)',
}
