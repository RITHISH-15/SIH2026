import html
import folium
from streamlit_folium import st_folium
import streamlit as st

def render_google_map(
    center_lat: float = 13.0827,
    center_lng: float = 80.2707,
    radius_km: int = 10,
    stations: list = None,
    reports: list = None,
    height: int = 520,
    key: str = "main_weather_folium_map"
):
    """
    Renders a clean, free interactive GIS map using standard OpenStreetMap tiles
    via folium and streamlit-folium. Centered on Chennai, Tamil Nadu (13.0827, 80.2707).
    No API keys required, no commercial watermarks.
    Features:
    - Standard OpenStreetMap base layer
    - Dynamic radius circle (1 km, 5 km, 10 km, 25 km) matching user selection
    - Physical weather stations (RMC Chennai, Open-Meteo Grid, Meenambakkam)
    - Incident report markers with status indicators and popups
    - Click-to-select location capture
    """
    # Create Folium map with standard OpenStreetMap tiles centered on Chennai
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=11,
        tiles="OpenStreetMap",
        control_scale=True
    )

    # 1. Dynamic Radius Circle
    folium.Circle(
        location=[center_lat, center_lng],
        radius=int(radius_km * 1000),
        color="#0284c7",
        fill=True,
        fill_color="#38bdf8",
        fill_opacity=0.18,
        weight=2,
        popup=folium.Popup(f"<b>Impact Perimeter</b><br/>Radius: {radius_km} km", max_width=200),
        tooltip=f"{radius_km} km Target Radius"
    ).add_to(m)

    # 2. Main Target Location Marker
    folium.Marker(
        location=[center_lat, center_lng],
        popup=folium.Popup(
            f"<b>📍 Selected Analysis Center</b><br/>"
            f"Latitude: {center_lat:.4f}<br/>"
            f"Longitude: {center_lng:.4f}<br/>"
            f"Radius: {radius_km} km",
            max_width=260
        ),
        tooltip="Selected Analysis Center",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # 3. Physical Weather Stations
    if not stations:
        stations = [
            {
                "name": "RMC Chennai (Nungambakkam)",
                "lat": 13.0594,
                "lng": 80.2444,
                "type": "IMD Official Station",
                "source": "RMC_Chennai_IMD",
                "temp": "32.0°C"
            },
            {
                "name": "Chennai (Open-Meteo Grid)",
                "lat": 13.0827,
                "lng": 80.2707,
                "type": "NWP Numerical Grid",
                "source": "Open-Meteo",
                "temp": "35.2°C"
            },
            {
                "name": "Meenambakkam Aviation Weather",
                "lat": 12.9856,
                "lng": 80.1693,
                "type": "Airport Met Office",
                "source": "IMD_Aviation",
                "temp": "31.5°C"
            }
        ]

    for stn in stations:
        popup_html = f"""
        <div style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 12px; line-height: 1.4; min-width: 180px;">
            <b style="color: #1e3a8a; font-size: 13px;">{html.escape(stn['name'])}</b><br/>
            <span style="color: #475569;">Type: <b>{html.escape(stn['type'])}</b></span><br/>
            <span style="color: #475569;">Source: <b>{html.escape(stn['source'])}</b></span><br/>
            <span style="color: #059669; font-weight: bold;">Live Temp: {stn.get('temp', 'N/A')}</span>
        </div>
        """
        folium.Marker(
            location=[stn["lat"], stn["lng"]],
            popup=folium.Popup(popup_html, max_width=240),
            tooltip=f"Station: {stn['name']}",
            icon=folium.Icon(color="blue", icon="cloud")
        ).add_to(m)

    # 4. Verified Incident Report Markers
    if reports:
        for r in reports[:20]:
            title = r.get("content_text") or r.get("title") or "Weather Incident"
            status = str(r.get("verification_status") or "UNVERIFIED").upper()
            hazard = r.get("hazard_category") or "Weather Report"
            url = r.get("source_url") or r.get("video_url") or "#"
            
            # Resolve coordinates or spread pseudo-geocodes around Chennai
            lat = r.get("latitude")
            lng = r.get("longitude")
            if not lat or not lng:
                title_hash = abs(hash(str(title)))
                lat = 13.0827 + ((title_hash % 41) - 20) * 0.0035
                lng = 80.2707 + (((title_hash // 41) % 41) - 20) * 0.0035

            # Choose marker color by verification status
            if "SUPPORTED" in status and "PARTIALLY" not in status:
                marker_color = "green"
                status_badge = "<span style='color: #059669; font-weight: bold;'>SUPPORTED</span>"
            elif "CONTRADICTED" in status:
                marker_color = "red"
                status_badge = "<span style='color: #dc2626; font-weight: bold;'>CONTRADICTED</span>"
            elif "PARTIALLY" in status:
                marker_color = "orange"
                status_badge = "<span style='color: #d97706; font-weight: bold;'>PARTIALLY SUPPORTED</span>"
            else:
                marker_color = "cadetblue"
                status_badge = "<span style='color: #64748b; font-weight: bold;'>UNVERIFIED</span>"

            rep_popup = f"""
            <div style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 12px; line-height: 1.4; min-width: 190px;">
                <b style="font-size: 13px;">{html.escape(str(title)[:45])}</b><br/>
                <span>Category: <b>{html.escape(str(hazard))}</b></span><br/>
                <span>Status: {status_badge}</span><br/>
                <a href="{url}" target="_blank" style="color: #2563eb; text-decoration: underline; font-weight: 600; display: inline-block; margin-top: 4px;">▶️ Watch Video</a>
            </div>
            """
            folium.Marker(
                location=[float(lat), float(lng)],
                popup=folium.Popup(rep_popup, max_width=240),
                tooltip=f"Report: {title[:30]} ({status})",
                icon=folium.Icon(color=marker_color, icon="facetime-video")
            ).add_to(m)

    # Render map using streamlit-folium with full container width
    map_output = st_folium(
        m,
        height=height,
        use_container_width=True,
        key=key,
        returned_objects=["last_clicked"]
    )

    # Interactive click coordinate readout
    if map_output and map_output.get("last_clicked"):
        clicked = map_output["last_clicked"]
        c_lat = clicked.get("lat")
        c_lng = clicked.get("lng")
        if c_lat is not None and c_lng is not None:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 8px; padding: 6px 12px; margin-top: 8px; font-size: 12px;">
                    <span style="color: #94a3b8;">Selected Coordinates:</span>
                    <span style="font-family: monospace; color: #38bdf8; font-weight: bold;">{c_lat:.4f}°N, {c_lng:.4f}°E</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    return map_output

# Alias for standard naming
render_map = render_google_map
