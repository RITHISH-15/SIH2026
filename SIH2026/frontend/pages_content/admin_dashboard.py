import streamlit as st
from services.supabase_service import get_database_statistics, trigger_pipeline

def render():
    """
    Renders the Admin Overview Dashboard.
    Displays live system metrics, total weather observations count,
    ingestion health, database status, and quick pipeline triggers.
    """
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #dc2626; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 800;">ADMIN</span>
                <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
                    System Telemetry & Big Data Operations Center
                </h2>
            </div>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
                Real-time monitor of PostgreSQL Supabase storage, pipeline workers, and automated ingestion health
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    stats = get_database_statistics()

    # 4 Main KPI Cards
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 12px; padding: 16px;">
                <div style="font-size: 11px; color: #94a3b8; font-weight: 700;">WEATHER OBSERVATIONS</div>
                <div style="font-size: 28px; font-weight: 800; color: #60a5fa; margin: 4px 0;">{stats['weather_count']:,}</div>
                <div style="font-size: 11px; color: #cbd5e1;">Latest: {stats['latest_weather_source']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(168, 85, 247, 0.4); border-radius: 12px; padding: 16px;">
                <div style="font-size: 11px; color: #94a3b8; font-weight: 700;">HAZARD PREDICTIONS</div>
                <div style="font-size: 28px; font-weight: 800; color: #c084fc; margin: 4px 0;">{stats['hazard_count']:,}</div>
                <div style="font-size: 11px; color: #cbd5e1;">7 Hazards Model Runs</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 12px; padding: 16px;">
                <div style="font-size: 11px; color: #94a3b8; font-weight: 700;">YOUTUBE REPORTS</div>
                <div style="font-size: 28px; font-weight: 800; color: #f87171; margin: 4px 0;">{stats['youtube_count']:,}</div>
                <div style="font-size: 11px; color: #cbd5e1;">Public Stream Ingested</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k4:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 16px;">
                <div style="font-size: 11px; color: #94a3b8; font-weight: 700;">VERIFIED SOCIAL DATA</div>
                <div style="font-size: 28px; font-weight: 800; color: #34d399; margin: 4px 0;">{stats['verified_count']:,}</div>
                <div style="font-size: 11px; color: #cbd5e1;">SHA-256 Deduplicated</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Ingestion Pipeline Health Cards
    st.markdown("### ⚙️ Ingestion Pipeline Orchestration")
    p1, p2 = st.columns(2)

    with p1:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(71, 85, 105, 0.3); border-radius: 12px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-weight: 700; font-size: 16px; color: #f8fafc;">📡 Open-Meteo Numerical Ingestion</div>
                    <span style="background: rgba(16,185,129,0.2); color: #34d399; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">ACTIVE</span>
                </div>
                <p style="font-size: 12px; color: #94a3b8; margin: 0 0 12px 0;">
                    Fetches 2m Temperature, Surface Pressure, Wind Speed/Direction, and Precipitation for Chennai (13.0827, 80.2707).
                </p>
                <div style="font-size: 11.5px; color: #cbd5e1; margin-bottom: 12px;">Script: <code>ingest_openmeteo.py</code></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🚀 Trigger Open-Meteo Ingestion", key="btn_run_openmeteo", use_container_width=True):
            with st.spinner("Executing ingest_openmeteo.py..."):
                res = trigger_pipeline("ingest_openmeteo.py")
                if res["success"]:
                    st.success("✅ Open-Meteo ingestion successful! New observation stored into weather_observations.")
                    st.code(res["stdout"])
                else:
                    st.error(f"❌ Ingestion failed with code {res['returncode']}")
                    st.code(res["stderr"] or res["stdout"])

    with p2:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(71, 85, 105, 0.3); border-radius: 12px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-weight: 700; font-size: 16px; color: #f8fafc;">🏛️ Regional Meteorological Centre (RMC) Scraper</div>
                    <span style="background: rgba(16,185,129,0.2); color: #34d399; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">ACTIVE</span>
                </div>
                <p style="font-size: 12px; color: #94a3b8; margin: 0 0 12px 0;">
                    Scrapes official live meteorological portal at mausam.imd.gov.in/chennai for Nungambakkam station.
                </p>
                <div style="font-size: 11.5px; color: #cbd5e1; margin-bottom: 12px;">Script: <code>ingest_rmc.py</code></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🚀 Trigger RMC IMD Ingestion", key="btn_run_rmc", use_container_width=True):
            with st.spinner("Executing ingest_rmc.py..."):
                res = trigger_pipeline("ingest_rmc.py")
                if res["success"]:
                    st.success("✅ RMC Chennai IMD scraper successful! Row stored into weather_observations.")
                    st.code(res["stdout"])
                else:
                    st.error(f"❌ Ingestion failed with code {res['returncode']}")
                    st.code(res["stderr"] or res["stdout"])
