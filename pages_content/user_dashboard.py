import streamlit as st
import textwrap
from services.supabase_service import (
    get_latest_weather_observation,
    get_latest_hazard_predictions,
    get_verified_social_reports,
    get_weather_history_data
)
from components.filters import render_filter_bar
from components.weather_cards import render_weather_cards
from components.hazard_cards import render_hazard_cards
from components.reports_view import render_reports_view
from components.google_map import render_google_map
from components.analytics_charts import render_alert_banner, render_hazard_radar_chart

def render():
    """
    Renders the Normal User Unified Dashboard.
    Combines live weather, 7 hazard ML predictions, map preview, and verified reports.
    """
    # 1. Filter Bar
    filters = render_filter_bar()

    # 2. Fetch Data
    with st.spinner("Fetching real-time weather & ML intelligence..."):
        weather = get_latest_weather_observation(source=filters["source"])
        hazards = get_latest_hazard_predictions(location=filters["location"])
        reports = get_verified_social_reports(
            status_filter=filters["verification"],
            hazard_filter=filters["hazard"],
            limit=6
        )

    # 3. Dynamic Alert Banner
    render_alert_banner(hazards)

    # 4. Live Weather Observation Cards
    render_weather_cards(weather)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 5. 7 Hazard Predictions Section
    render_hazard_cards(hazards)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 6. Map and Hazard Radar side by side
    map_col, radar_col = st.columns([6, 4])
    
    with map_col:
        header_map = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
    <h4 style="margin: 0; font-size: 16px; font-weight: 700; color: #f8fafc;">
        🗺️ Interactive Weather GIS Map
    </h4>
    <span style="font-size: 11px; color: #38bdf8;">Radius: {filters['radius_km']} km</span>
</div>
"""
        st.markdown(textwrap.dedent(header_map).strip(), unsafe_allow_html=True)
        render_google_map(
            center_lat=13.0827,
            center_lng=80.2707,
            radius_km=filters["radius_km"],
            reports=reports,
            height=420,
            key="dashboard_weather_map"
        )

    with radar_col:
        render_hazard_radar_chart(hazards)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # 7. Recent Verified Reports Section
    render_reports_view(reports, title="Latest Verified Social & YouTube Weather Reports")
