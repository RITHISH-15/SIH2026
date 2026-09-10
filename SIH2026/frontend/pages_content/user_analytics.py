import streamlit as st
import pandas as pd
from services.supabase_service import (
    get_weather_history_data,
    get_latest_hazard_predictions,
    get_verified_social_reports
)
from components.analytics_charts import (
    render_weather_trends_chart,
    render_hazard_radar_chart,
    render_verification_donut_chart,
    render_alert_banner
)

def render():
    """
    Renders Big Data Analytics & Alerts page.
    """
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
                📊 Big Data Weather Analytics & Alert Center
            </h2>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
                Longitudinal telemetry analysis over 26,000+ atmospheric records and ML risk correlations
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    hazards = get_latest_hazard_predictions()
    render_alert_banner(hazards)

    # Top Analytics Tabs
    tab_overview, tab_hazards, tab_verification = st.tabs([
        "📈 Big Data Weather Profiles",
        "🎯 Hazard Radar & Distributions",
        "🛡️ Verification Reliability Metrics"
    ])

    with tab_overview:
        history_data = get_weather_history_data(limit=500)
        render_weather_trends_chart(history_data)

    with tab_hazards:
        col_rad, col_expl = st.columns([6, 4])
        with col_rad:
            render_hazard_radar_chart(hazards)
        with col_expl:
            st.markdown(
                """
                <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(71,85,105,0.3); border-radius: 12px; padding: 16px;">
                    <h4 style="margin: 0 0 8px 0; color: #38bdf8;">ML Hazard Confidence Thresholds</h4>
                    <p style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
                        The SIH 2026 pipeline evaluates 7 atmospheric hazard vectors using calibrated gradient-boosted decision trees trained on historical IMD Chennai weather extremes.
                    </p>
                    <ul style="font-size: 12px; color: #94a3b8; padding-left: 18px;">
                        <li><strong>Low Risk (&lt; 30%)</strong>: Standard atmospheric conditions.</li>
                        <li><strong>Medium Risk (30% - 60%)</strong>: Early watch advisory triggers sensor polling frequency increase.</li>
                        <li><strong>High Risk (&gt; 60%)</strong>: Red warning dispatched to municipal emergency systems.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab_verification:
        reports = get_verified_social_reports(limit=50)
        col_don, col_desc = st.columns([5, 5])
        with col_don:
            render_verification_donut_chart(reports)
        with col_desc:
            st.markdown(
                """
                <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(71,85,105,0.3); border-radius: 12px; padding: 16px;">
                    <h4 style="margin: 0 0 8px 0; color: #34d399;">Multimodal Cross-Verification Protocol</h4>
                    <p style="font-size: 12px; color: #cbd5e1; line-height: 1.5;">
                        Citizen-reported videos on social platforms are automatically deduplicated via SHA-256 fingerprinting and cross-referenced with nearest physical rain gauge records:
                    </p>
                    <ul style="font-size: 12px; color: #94a3b8; padding-left: 18px;">
                        <li><strong style="color: #34d399;">SUPPORTED</strong>: Heavy rain claims corroborated by &gt; 5.0mm physical gauge precipitation.</li>
                        <li><strong style="color: #60a5fa;">PARTIALLY_SUPPORTED</strong>: Surrounding radar reflects convective clouds, but local station rainfall is minimal.</li>
                        <li><strong style="color: #f87171;">CONTRADICTED</strong>: Flood/rain claim with 0.0mm recorded rain and clear satellite imagery (potential old/misleading footage).</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
