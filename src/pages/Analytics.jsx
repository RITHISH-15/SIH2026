import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import AdminSidebar from '../components/AdminSidebar'
import StatCard from '../components/StatCard'
import { dailyVolume, typeBreakdown, districtVolumes } from '../data/mockData'

export default function Analytics() {
  return (
    <div style={{ display: 'flex' }}>
      <AdminSidebar active="/admin/analytics" />
      <div style={{ flex: 1, padding: '24px 28px', maxWidth: 1180 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 18 }}>
          <div>
            <h1 style={{ fontSize: 21 }}>Analytics &amp; telemetry insights</h1>
            <div style={{ fontSize: 13, color: 'var(--text-500)' }}>Aggregated from the verified event store · refreshed every few minutes</div>
          </div>
          <button className="btn btn-ghost">⬇ Export PDF summary</button>
        </div>

        <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
          <StatCard label="Total reports" value="48,290" sub="+930 today" />
          <StatCard label="Verified %" value="91.4%" accent="var(--teal-600)" />
          <StatCard label="Avg. verification time" value="1.6 min" />
          <StatCard label="Flagged rate" value="3.2%" accent="var(--red-600)" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.3fr 1fr', gap: 16, marginBottom: 16 }}>
          <div className="card" style={{ padding: 18 }}>
            <h3 style={{ fontSize: 14, marginBottom: 14 }}>Submitted vs. verified — last 7 days</h3>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={dailyVolume}>
                <CartesianGrid stroke="var(--border)" vertical={false} />
                <XAxis dataKey="day" tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
                <Tooltip />
                <Line type="monotone" dataKey="submitted" stroke="var(--navy-500)" strokeWidth={2} dot={false} name="Submitted" />
                <Line type="monotone" dataKey="verified" stroke="var(--teal-600)" strokeWidth={2} dot={false} name="Verified" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="card" style={{ padding: 18 }}>
            <h3 style={{ fontSize: 14, marginBottom: 14 }}>Events by type today</h3>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={typeBreakdown} layout="vertical" margin={{ left: 20 }}>
                <XAxis type="number" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="type" tick={{ fontSize: 11 }} width={150} axisLine={false} tickLine={false} />
                <Tooltip />
                <Bar dataKey="count" fill="var(--blue-accent)" radius={[0, 4, 4, 0]} barSize={14} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card" style={{ padding: 18 }}>
          <h3 style={{ fontSize: 14, marginBottom: 14 }}>Top districts by reporting volume</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr 1fr', fontSize: 11.5, fontWeight: 700, color: 'var(--text-500)', padding: '0 4px 8px' }}>
            <div>DISTRICT</div>
            <div>TOTAL REPORTS</div>
            <div>VERIFIED %</div>
          </div>
          {districtVolumes.map((s) => (
            <div key={s.district} style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr 1fr', alignItems: 'center', padding: '10px 4px', borderTop: '1px solid var(--border)', fontSize: 13.5 }}>
              <div style={{ fontWeight: 600 }}>{s.district}</div>
              <div>{s.reports.toLocaleString()}</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div style={{ width: 80, height: 6, borderRadius: 3, background: 'var(--surface-sunken)' }}>
                  <div style={{ width: `${s.verifiedPct}%`, height: '100%', borderRadius: 3, background: 'var(--teal-600)' }} />
                </div>
                {s.verifiedPct}%
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
