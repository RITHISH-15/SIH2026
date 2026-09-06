import { STATUS } from '../data/mockData'

const COPY = {
  [STATUS.VERIFIED]: 'Verified ground truth',
  [STATUS.REVIEW]: 'Under peer review',
  [STATUS.FLAGGED]: 'Flagged / disputed',
}

const CLASS = {
  [STATUS.VERIFIED]: 'badge-verified',
  [STATUS.REVIEW]: 'badge-review',
  [STATUS.FLAGGED]: 'badge-flagged',
}

export default function StatusBadge({ status, compact = false }) {
  return (
    <span className={`badge ${CLASS[status]}`}>
      <span className="badge-dot" />
      {compact ? COPY[status].split(' ')[0] : COPY[status]}
    </span>
  )
}
