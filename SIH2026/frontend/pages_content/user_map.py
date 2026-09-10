import streamlit as st
import textwrap
from services.supabase_service import get_verified_social_reports
from components.google_map import render_google_map

def render():
    """
    Renders the dedicated Full-Screen Interactive Weather Map Page using Folium & OpenStreetMap.
    """
    header_html = """
<div style="margin-bottom: 16px;">
    <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
        🗺️ Geospatial Weather & Hazard Radar Map
    </h2>
    <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
        Interactive GIS mapping powered by Folium and OpenStreetMap with dynamic radius circles, IMD stations, and verified incident markers
    </p>
</div>
"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # Control Bar
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    with col1:
        target_place = st.selectbox(
            "Quick Navigate Zone:",
            [
                "Chennai Central (13.0827, 80.2707)",
                "Nungambakkam IMD (13.0594, 80.2444)",
                "Meenambakkam Airport (12.9856, 80.1693)",
                "Tambaram (12.9249, 80.1000)"
            ]
        )
    with col2:
        radius_km = st.selectbox("Search & Impact Radius:", [1, 5, 10, 25], index=2, format_func=lambda x: f"{x} km")
    with col3:
        map_layer = st.multiselect(
            "Active Map Overlays:",
            ["Physical Sensors", "Verified Reports", "Radius Perimeter"],
            default=["Physical Sensors", "Verified Reports", "Radius Perimeter"]
        )
    with col4:
        st.write("")
        if st.button("📍 Re-Center Map", use_container_width=True):
            st.rerun()

    # Determine lat, lng
    if "Nungambakkam" in target_place:
        lat, lng = 13.0594, 80.2444
    elif "Meenambakkam" in target_place:
        lat, lng = 12.9856, 80.1693
    elif "Tambaram" in target_place:
        lat, lng = 12.9249, 80.1000
    else:
        lat, lng = 13.0827, 80.2707

    # Fetch incident reports for map plotting
    reports = get_verified_social_reports(limit=25) if "Verified Reports" in map_layer else []

    # Render Map Component
    render_google_map(
        center_lat=lat,
        center_lng=lng,
        radius_km=radius_km,
        reports=reports,
        height=580,
        key="fullscreen_weather_map"
    )

    # Map Legend & Instructions
    legend_html = """
<div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(71, 85, 105, 0.3); border-radius: 10px; padding: 12px 18px; margin-top: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
    <div style="font-size: 12px; color: #cbd5e1;">
        <strong>Interactive Controls:</strong> Click anywhere on the map to select coordinates or view station/report telemetry popups.
    </div>
    <div style="display: flex; gap: 16px; font-size: 12px;">
        <span style="color: #60a5fa;">🔵 Weather Station</span>
        <span style="color: #34d399;">🟢 Supported Report</span>
        <span style="color: #f87171;">🔴 Contradicted Report</span>
        <span style="color: #fbbf24;">🟡 Partially Supported / Unverified</span>
    </div>
</div>
"""
    st.markdown(textwrap.dedent(legend_html).strip(), unsafe_allow_html=True)
