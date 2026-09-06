import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AdminSidebar from '../components/AdminSidebar'
import StatusBadge from '../components/StatusBadge'
import StatCard from '../components/StatCard'
import { reports, EVENT_TYPES } from '../data/mockData'

export default function Archive() {
  const [query, setQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const navigate = useNavigate()

  const filtered = useMemo(() => {
    return reports.filter((r) => {
      if (statusFilter !== 'all' && r.status !== statusFilter) return false
      if (query && !`${r.title} ${r.area}`.toLowerCase().includes(query.toLowerCase())) return false
      return true
    })
  }, [query, statusFilter])

  function exportCsv() {
    const header = 'id,title,area,type,status,score,reported\n'
    const rows = filtered.map((r) => `${r.id},"${r.title}",${r.area},${r.type},${r.status},${r.score},"${r.reportedAgo}"`).join('\n')
    const blob = new Blob([header + rows], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'weathertrust_reports_export.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div style={{ display: 'flex' }}>
      <AdminSidebar active="/admin/archive" />
      <div style={{ flex: 1, padding: '24px 28px', maxWidth: 1180 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 18 }}>
          <div>
            <h1 style={{ fontSize: 21 }}>Historical reports archive</h1>
            <div style={{ fontSize: 13, color: 'var(--text-500)' }}>Every report ever submitted — verified, rejected, or hidden. Nothing is silently deleted.</div>
          </div>
          <button className="btn btn-accent" onClick={exportCsv}>⬇ Export CSV</button>
        </div>

        <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
          <StatCard label="Total archived" value="48,290" />
          <StatCard label="Verified" value="44,137" accent="var(--teal-600)" />
          <StatCard label="Rejected / hidden" value="4,153" accent="var(--red-600)" />
          <StatCard label="Audit trail coverage" value="100%" />
        </div>

        <div style={{ display: 'flex', gap: 10, marginBottom: 14 }}>
          <input
            className="input"
            placeholder="Search by title, area, or location..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ maxWidth: 340 }}
          />
          {['all', 'verified', 'review', 'flagged'].map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={statusFilter === s ? 'btn btn-primary' : 'btn btn-ghost'}
              style={{ textTransform: 'capitalize' }}
            >
              {s}
            </button>
          ))}
        </div>

        <div className="card">
          <div style={{ display: 'grid', gridTemplateColumns: '2.2fr 1fr 1fr 1fr', padding: '10px 18px', fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)', borderBottom: '1px solid var(--border)' }}>
            <div>REPORT</div>
            <div>EVENT TYPE</div>
            <div>STATUS</div>
            <div>TIMESTAMP</div>
          </div>
          {filtered.map((r) => {
            const meta = EVENT_TYPES.find((t) => t.key === r.type)
            return (
              <div
                key={r.id}
                onClick={() => navigate(`/event/${r.id}`)}
                style={{ display: 'grid', gridTemplateColumns: '2.2fr 1fr 1fr 1fr', alignItems: 'center', padding: '12px 18px', borderBottom: '1px solid var(--border)', cursor: 'pointer' }}
              >
                <div style={{ display: 'flex', gap: 10, alignItems: 'center', minWidth: 0 }}>
                  <img src={r.thumb} alt="" style={{ width: 38, height: 38, borderRadius: 8, objectFit: 'cover' }} />
                  <div style={{ minWidth: 0 }}>
                    <div style={{ fontSize: 13, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{r.title}</div>
                    <div style={{ fontSize: 11.5, color: 'var(--text-500)' }}>{r.area} · {r.id}</div>
                  </div>
                </div>
                <div style={{ fontSize: 13 }}>{meta?.icon} {meta?.label}</div>
                <div><StatusBadge status={r.status} compact /></div>
                <div style={{ fontSize: 12.5, color: 'var(--text-500)' }}>{r.reportedAgo}</div>
              </div>
            )
          })}
          {filtered.length === 0 && (
            <div style={{ padding: 30, textAlign: 'center', fontSize: 13.5, color: 'var(--text-500)' }}>No archived reports match this search.</div>
          )}
        </div>
      </div>
    </div>
  )
}
