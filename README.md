# WeatherTrust — Verified Weather Event Reporting Platform

A full React + Vite prototype of a citizen weather-reporting & verification
platform, mapped around **Chennai and its surrounding districts**. Built to
mirror the reference screenshots: a public trust dashboard with a live map
and feed, plus a dark-navy admin console for verification, analytics, and
audit.

## Run it

```bash
npm install
npm run dev
```

Then open the printed local URL (typically `http://localhost:5173`).

To build a static production bundle:

```bash
npm run build
npm run preview
```

## Pages (all linked together)

| # | Route | Page |
|---|---|---|
| 1 | `/` | Home / Public Dashboard — live map, filters, live feed |
| 2 | `/event/:id` | Event Detail — evidence, telemetry, nearby reports |
| 3 | `/report` | Report an Event — 4-step upload → location → type → description |
| 4 | `/admin/queue` | Verification Queue (admin) — approve/reject with score drawer |
| 5 | `/admin/analytics` | Analytics (admin) — charts & state leaderboard |
| 6 | `/admin/archive` | Reports Archive (admin) — search, filter, CSV export |
| 7 | `/about` | About / How It Works — static pipeline explainer + FAQ |
| 8 | `/login` | Admin login |
| 9 | `/admin/redzone/:id` | Red Zone Fact-Check — claim vs. ground-truth comparison |

## Notes on the data layer

Everything currently reads from `src/data/mockData.js` — a set of realistic
Chennai-area reports (Kotturpuram, Velachery, Sholinganallur, Thiruvanmiyur,
Tambaram, Red Hills, etc.) with lat/lng, credibility scores, and telemetry.
The "live feed" and WebSocket-style updates on the dashboard are simulated
with a timer. To wire this to a real backend:

- Replace the imports from `mockData.js` with `fetch`/`axios` calls to your API.
- Swap the `setInterval` ticker in `Dashboard.jsx` for a real WebSocket subscription.
- `ReportEvent.jsx`'s `submit()` is where you'd `POST` to your ingestion pipeline.
- `VerificationQueue.jsx`'s `decide()` is where Approve/Reject would `PATCH` report status.

## Stack

- React 18 + React Router (hash routing, so it works from a plain static file host)
- Leaflet / react-leaflet for the map (OpenStreetMap tiles)
- Recharts for the analytics charts
- Plain CSS with design tokens in `src/index.css` (no framework) — colors,
  radii, and shadows are all defined as CSS variables so the theme is easy
  to retint.
