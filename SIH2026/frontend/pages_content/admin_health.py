import time
import streamlit as st
from services.supabase_service import get_supabase_client, get_database_statistics

def render():
    """
    Renders System Health, Connection Diagnostics, and Latency Probing view.
    """
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #dc2626; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 800;">ADMIN</span>
                <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
                    System Health & Infrastructure Diagnostics
                </h2>
            </div>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
                Network round-trip latency, PostgreSQL connection status, and schema integrity
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Ping database and measure latency
    start_time = time.time()
    try:
        client = get_supabase_client()
        ping_res = client.table("weather_observations").select("id").limit(1).execute()
        latency_ms = (time.time() - start_time) * 1000
        is_healthy = True
        status_msg = "Operational - Low Latency"
    except Exception as e:
        latency_ms = -1
        is_healthy = False
        status_msg = f"Connection Failed: {e}"

    stats = get_database_statistics()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(16,185,129,0.3); border-radius: 12px; padding: 16px;">
                <div style="font-size: 11px; color: #94a3b8; font-weight: 700;">DATABASE STATUS</div>
                <div style="font-size: 24px; font-weight: 800; color: {'#34d399' if is_healthy else '#f87171'}; margin: 4px 0;">
                    {'🟢 ONLINE' if is_healthy else '🔴 OFFLINE'}
                </div>
                <div style="font-size: 11px; color: #cbd5e1;">{status_msg}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        lat_color = "#34d399" if latency_ms < 300 else "#fbbf24" if latency_ms < 800 else "#f87171"
        st.markdown(
            f"""
            <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(59,130,246,0.3); border-radius: 12px; padding: 16px;">
                <div style="font-size: 11px; color: #94a3b8; font-weight: 700;">PING LATENCY</div>
                <div style="font-size: 24px; font-weight: 800; color: {lat_color}; margin: 4px 0;">
                    {latency_ms:.1f} ms
                </div>
                <div style="font-size: 11px; color: #cbd5e1;">Supabase Cloud Region</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(168,85,247,0.3); border-radius: 12px; padding: 16px;">
                <div style="font-size: 11px; color: #94a3b8; font-weight: 700;">TOTAL BIG DATA ROWS</div>
                <div style="font-size: 24px; font-weight: 800; color: #c084fc; margin: 4px 0;">
                    {(stats['weather_count'] + stats['hazard_count'] + stats['youtube_count'] + stats['verified_count']):,}
                </div>
                <div style="font-size: 11px; color: #cbd5e1;">Across 4 Managed Tables</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Detailed Table Breakdown
    st.markdown("### 📊 Database Storage & Table Inventory")
    st.markdown(
        f"""
        | PostgreSQL Table Name | Entity Description | Record Count | Primary Ingestion Pipeline |
        | :--- | :--- | :---: | :--- |
        | `weather_observations` | Surface Atmospheric Readings & Numerical Forecasts | **{stats['weather_count']:,}** | `ingest_openmeteo.py` & `ingest_rmc.py` |
        | `hazard_predictions` | 7-Vector Hazard ML Operational Inference | **{stats['hazard_count']:,}** | `hazard_prediction_model.pkl` |
        | `public_youtube_reports` | Raw Scraped YouTube Weather Reports | **{stats['youtube_count']:,}** | YouTube API Collector |
        | `verified_social_reports`| Multimodal Cross-Verified Incidents with SHA-256 | **{stats['verified_count']:,}** | Verification Engine |
        """
    )
