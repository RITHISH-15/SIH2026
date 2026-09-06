import { Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import EventDetail from './pages/EventDetail'
import ReportEvent from './pages/ReportEvent'
import About from './pages/About'
import Login from './pages/Login'
import VerificationQueue from './pages/VerificationQueue'
import Analytics from './pages/Analytics'
import Archive from './pages/Archive'
import RedZoneFactCheck from './pages/RedZoneFactCheck'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/event/:id" element={<EventDetail />} />
      <Route path="/report" element={<ReportEvent />} />
      <Route path="/about" element={<About />} />
      <Route path="/login" element={<Login />} />

      <Route path="/admin/queue" element={<VerificationQueue />} />
      <Route path="/admin/analytics" element={<Analytics />} />
      <Route path="/admin/archive" element={<Archive />} />
      <Route path="/admin/redzone/:id" element={<RedZoneFactCheck />} />

      <Route path="*" element={<Dashboard />} />
    </Routes>
  )
}
