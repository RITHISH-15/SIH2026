import { useEffect, useMemo, useState } from 'react'
import TopNav from '../components/TopNav'
import MapView from '../components/MapView'
import FilterChip from '../components/FilterChip'
import EventCard from '../components/EventCard'
import StatusBadge from '../components/StatusBadge'
import { reports as allReports, EVENT_TYPES, STATUS, feedTicker } from '../data/mockData'

export default function Dashboard() {
  const [typeFilter, setTypeFilter] = useState(null)
  const [statusFilter, setStatusFilter] = useState(null)
  const [window_, setWindow] = useState('24h')
  const [liveFeed, setLiveFeed] = useState(allReports.slice(0, 6))
  const [tick, setTick] = useState(0)

  // Simulate a live WebSocket feed: every few seconds, promote the next
  // ticker item to the top of the live feed with a fade-in.
  useEffect(() => {
    const interval = setInterval(() => {
      setTick((t) => (t + 1) % feedTicker.length)
    }, 6000)
    return () => clearInterval(interval)
  }, [])

  const filtered = useMemo(() => {
    return allReports.filter((r) => {
      if (typeFilter && r.type !== typeFilter) return false
      if (statusFilter && r.status !== statusFilter) return false
      return true
    })
  }, [typeFilter, statusFilter])

  const counts = useMemo(() => {
    const c = {}
    EVENT_TYPES.forEach((t) => { c[t.key] = allReports.filter((r) => r.type === t.key).length })
    return c
  }, [])

  const statusCounts = {
    [STATUS.VERIFIED]: allReports.filter((r) => r.status === STATUS.VERIFIED).length,
    [STATUS.REVIEW]: allReports.filter((r) => r.status === STATUS.REVIEW).length,
    [STATUS.FLAGGED]: allReports.filter((r) => r.status === STATUS.FLAGGED).length,
  }

  return (
    <div>
      <TopNav />

      <div style={{ maxWidth: 1360, margin: '0 auto', padding: '20px 24px 60px', display: 'grid', gridTemplateColumns: '240px 1fr 320px', gap: 18 }}>
        {/* ------- left filter rail ------- */}
        <div>
          <div className="card" style={{ padding: 14, marginBottom: 14 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
              <span style={{ fontSize: 13, fontWeight: 700 }}>Filter feed</span>
              <button
                onClick={() => { setTypeFilter(null); setStatusFilter(null) }}
                style={{ background: 'none', border: 'none', color: 'var(--blue-accent)', fontSize: 12, fontWeight: 600, cursor: 'pointer' }}
              >
                Reset all
              </button>
            </div>

            <div style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)', margin: '10px 0 6px' }}>EVENT TYPE</div>
            {EVENT_TYPES.map((t) => (
              <FilterChip
                key={t.key}
                label={`${t.icon} ${t.label}`}
                count={counts[t.key]}
                active={typeFilter === t.key}
                onClick={() => setTypeFilter(typeFilter === t.key ? null : t.key)}
              />
            ))}

            <div style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)', margin: '14px 0 6px' }}>VERIFICATION STATUS</div>
            <FilterChip label="Verified ground truth" color="#0e9a72" count={statusCounts[STATUS.VERIFIED]} active={statusFilter === STATUS.VERIFIED} onClick={() => setStatusFilter(statusFilter === STATUS.VERIFIED ? null : STATUS.VERIFIED)} />
            <FilterChip label="Under peer review" color="#c9820f" count={statusCounts[STATUS.REVIEW]} active={statusFilter === STATUS.REVIEW} onClick={() => setStatusFilter(statusFilter === STATUS.REVIEW ? null : STATUS.REVIEW)} />
            <FilterChip label="Flagged / disputed" color="#d3342b" count={statusCounts[STATUS.FLAGGED]} active={statusFilter === STATUS.FLAGGED} onClick={() => setStatusFilter(statusFilter === STATUS.FLAGGED ? null : STATUS.FLAGGED)} />

            <div style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)', margin: '14px 0 6px' }}>OBSERVATION WINDOW</div>
            {['24 hours', '3 days', '7 days'].map((w) => (
              <FilterChip key={w} label={w} active={window_ === w} onClick={() => setWindow(w)} />
            ))}
          </div>

          <div className="card" style={{ padding: 14, textAlign: 'center' }}>
            <div style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)' }}>TAMIL NADU TRUST INDEX</div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: 30, fontWeight: 700, color: 'var(--teal-600)', margin: '6px 0 2px' }}>98.4%</div>
            <div style={{ fontSize: 11.5, color: 'var(--text-500)' }}>Confidence · IMD Chennai ground-truth agreement</div>
          </div>
        </div>

        {/* ------- center map ------- */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 10 }}>
            <div>
              <h1 style={{ fontSize: 22 }}>Live verification map</h1>
              <div style={{ fontSize: 13, color: 'var(--text-500)' }}>Chennai Metropolitan Area &amp; surrounding districts</div>
            </div>
            <div style={{ fontSize: 12, color: 'var(--text-500)', display: 'flex', alignItems: 'center', gap: 6 }}>
              <span style={{ width: 7, height: 7, borderRadius: '50%', background: 'var(--teal-600)', animation: 'pulseDot 1.6s infinite' }} />
              Sync 14s ago
            </div>
          </div>

          <MapView reports={filtered} height={440} />

          <div style={{ display: 'flex', gap: 12, marginTop: 14 }}>
            <div className="card" style={{ padding: 14, flex: 1 }}>
              <div style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)' }}>TOTAL REPORTS TODAY</div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: 24, fontWeight: 700, margin: '4px 0' }}>3,576</div>
              <div style={{ height: 6, borderRadius: 3, background: 'var(--surface-sunken)', overflow: 'hidden', display: 'flex' }}>
                <div style={{ width: '79%', background: 'var(--teal-600)' }} />
                <div style={{ width: '18%', background: 'var(--amber-600)' }} />
                <div style={{ width: '3%', background: 'var(--red-600)' }} />
              </div>
              <div style={{ fontSize: 11.5, color: 'var(--text-500)', marginTop: 6 }}>79% verified · 18% in review · 3% flagged</div>
            </div>
            <div className="card" style={{ padding: 14, flex: 1 }}>
              <div style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)' }}>CONNECTED GROUND NODES</div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: 24, fontWeight: 700, margin: '4px 0' }}>58,420</div>
              <div style={{ fontSize: 11.5, color: 'var(--text-500)' }}>AWS / ARC stations · 37 Doppler radars operational</div>
            </div>
          </div>
        </div>

        {/* ------- right live feed ------- */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <span style={{ fontSize: 13, fontWeight: 700 }}>Live reports</span>
            <span style={{ fontSize: 11.5, color: 'var(--teal-600)', display: 'flex', alignItems: 'center', gap: 5 }}>
              <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--teal-600)' }} /> Live
            </span>
          </div>

          <div key={tick} style={{ animation: 'feedIn 0.4s ease' }}>
            <div className="card" style={{ padding: '10px 12px', marginBottom: 10, borderColor: 'var(--blue-accent)' }}>
              <div style={{ fontSize: 12, color: 'var(--text-500)' }}>{feedTicker[tick].ago}</div>
              <div style={{ fontSize: 13.5, fontWeight: 600, margin: '2px 0' }}>
                New report · {feedTicker[tick].area}
              </div>
              <div style={{ fontSize: 12, color: 'var(--text-500)' }}>Awaiting classification…</div>
            </div>
          </div>

          <div className="scrollbar-thin" style={{ maxHeight: 560, overflowY: 'auto' }}>
            {filtered.map((r) => <EventCard key={r.id} report={r} />)}
            {filtered.length === 0 && (
              <div className="card" style={{ padding: 20, textAlign: 'center', fontSize: 13, color: 'var(--text-500)' }}>
                No reports match these filters right now.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
