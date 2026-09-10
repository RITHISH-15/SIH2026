import streamlit as st
import pandas as pd
from services.supabase_service import (
    get_latest_weather_observation,
    get_recent_weather_observations,
    get_weather_history_data
)
from components.weather_cards import render_weather_cards
from components.analytics_charts import render_weather_trends_chart

def render():
    """
    Renders the Live Weather Deep-Dive Page.
    """
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
                🌦️ Live Weather Observation Network
            </h2>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
                Real-time surface meteorology synced from Open-Meteo API and RMC Chennai IMD portal
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Station Source Selector
    c1, c2 = st.columns([3, 1])
    with c1:
        source_sel = st.radio(
            "Select Weather Data Stream:",
            ["ALL", "Open-Meteo", "RMC_Chennai_IMD"],
            horizontal=True
        )
    with c2:
        st.write("")
        if st.button("🔄 Poll Sensors Now", use_container_width=True):
            st.rerun()

    # Latest Observation
    latest_obs = get_latest_weather_observation(source=source_sel)
    render_weather_cards(latest_obs)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Historical Big Data Trends
    st.markdown("### 📈 Multi-Sensor Historical Weather Trends")
    history_data = get_weather_history_data(limit=300, source=source_sel)
    render_weather_trends_chart(history_data)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Recent Ingested Observations Table
    st.markdown("### 📋 Recent Station Ingestion Stream")
    recent_records = get_recent_weather_observations(limit=10)
    if recent_records:
        df_recent = pd.DataFrame(recent_records)[[
            "id", "station_name", "temperature_c", "humidity_percent",
            "wind_speed_kmph", "pressure_hpa", "rainfall_24h_mm", "source", "retrieved_at"
        ]]
        df_recent.columns = [
            "ID", "Station", "Temp (°C)", "Humidity (%)",
            "Wind (km/h)", "Pressure (hPa)", "Rain 24h (mm)", "Source", "Ingested At"
        ]
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
