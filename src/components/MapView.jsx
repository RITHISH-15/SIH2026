import { MapContainer, TileLayer, CircleMarker, Tooltip, useMap } from 'react-leaflet'
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { CHENNAI_CENTER, STATUS } from '../data/mockData'

const COLORS = {
  [STATUS.VERIFIED]: '#0e9a72',
  [STATUS.REVIEW]: '#c9820f',
  [STATUS.FLAGGED]: '#d3342b',
}

function Recenter({ center }) {
  const map = useMap()
  useEffect(() => {
    map.setView(center, map.getZoom())
  }, [center])
  return null
}

export default function MapView({ reports, height = 420, center = CHENNAI_CENTER, zoom = 11 }) {
  const navigate = useNavigate()
  return (
    <div style={{ height, borderRadius: 12, overflow: 'hidden', border: '1px solid var(--border)' }}>
      <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Recenter center={center} />
        {reports.map((r) => (
          <CircleMarker
            key={r.id}
            center={[r.lat, r.lng]}
            radius={9}
            pathOptions={{ color: '#fff', weight: 2, fillColor: COLORS[r.status], fillOpacity: 0.95 }}
            eventHandlers={{ click: () => navigate(`/event/${r.id}`) }}
          >
            <Tooltip direction="top" offset={[0, -6]}>
              <strong>{r.area}</strong>
              <br />
              {r.title}
            </Tooltip>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  )
}
