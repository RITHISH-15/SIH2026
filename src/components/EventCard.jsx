import { useNavigate } from 'react-router-dom'
import StatusBadge from './StatusBadge'
import { EVENT_TYPES } from '../data/mockData'

export default function EventCard({ report, compact = false }) {
  const navigate = useNavigate()
  const meta = EVENT_TYPES.find((t) => t.key === report.type)
  return (
    <button
      onClick={() => navigate(`/event/${report.id}`)}
      style={{
        display: 'flex', gap: 10, width: '100%', textAlign: 'left',
        padding: compact ? '10px 12px' : '12px 14px',
        border: '1px solid var(--border)', borderRadius: 10, background: '#fff',
        cursor: 'pointer', marginBottom: 8,
      }}
    >
      <img
        src={report.thumb}
        alt=""
        style={{ width: 52, height: 52, borderRadius: 8, objectFit: 'cover', flexShrink: 0 }}
      />
      <div style={{ minWidth: 0, flex: 1 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
          <span style={{ fontSize: 13.5, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {meta?.icon} {report.area}
          </span>
          <span style={{ fontSize: 11.5, color: 'var(--text-500)', flexShrink: 0 }}>{report.reportedAgo}</span>
        </div>
        <div style={{ fontSize: 12.5, color: 'var(--text-500)', margin: '3px 0 6px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {report.title}
        </div>
        <StatusBadge status={report.status} compact />
      </div>
    </button>
  )
}
