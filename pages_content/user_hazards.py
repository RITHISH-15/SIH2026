import streamlit as st
import textwrap
import pandas as pd
import plotly.express as px
from services.supabase_service import get_latest_hazard_predictions
from components.hazard_cards import render_hazard_cards, HAZARD_CONFIG
from components.analytics_charts import render_hazard_radar_chart

def render():
    """
    Renders the 7 Hazard Predictions Intelligence Page.
    """
    header_html = """
<div style="margin-bottom: 16px;">
    <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
        ⚠️ 7-Vector Hazard Early Warning System
    </h2>
    <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
        Predictive risk modeling across 7 severe weather categories powered by hazard_prediction_model.pkl
    </p>
</div>
"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # Location picker
    col1, col2 = st.columns([3, 1])
    with col1:
        loc = st.selectbox("Select Target Urban Zone:", ["Chennai", "North Chennai", "South Chennai", "Tambaram", "Sriperumbudur"])
    with col2:
        st.write("")
        if st.button("🔄 Refresh Prediction", use_container_width=True):
            st.rerun()

    hazards = get_latest_hazard_predictions(location=loc)

    # Render Cards (renders the 7 hazard cards cleanly)
    render_hazard_cards(hazards)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Detailed Analysis Section
    c_radar, c_bar = st.columns([5, 5])
    with c_radar:
        render_hazard_radar_chart(hazards)
    with c_bar:
        preds = hazards.get("predictions", {})
        data = []
        for k in ["rainfall", "thunderstorm", "flooding", "heatwave", "fog", "dust_storm", "strong_wind"]:
            prob = preds.get(k, {}).get("probability", 0.0)
            data.append({
                "Hazard": HAZARD_CONFIG.get(k, {}).get("title", k.title()),
                "Probability (%)": prob * 100 if prob <= 1.0 else prob,
                "Risk Tier": str(preds.get(k, {}).get("risk_level", "LOW")).upper()
            })
        df_haz = pd.DataFrame(data)
        fig_bar = px.bar(
            df_haz,
            x="Hazard",
            y="Probability (%)",
            color="Risk Tier",
            color_discrete_map={"LOW": "#10b981", "MEDIUM": "#f59e0b", "HIGH": "#ef4444"},
            title="7 Hazards Risk Level Comparison",
            text_auto=".1f"
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(15,23,42,0)",
            plot_bgcolor="rgba(30,41,59,0.4)",
            font=dict(color="#cbd5e1"),
            yaxis=dict(range=[0, 100], gridcolor="rgba(71,85,105,0.2)"),
            xaxis=dict(gridcolor="rgba(71,85,105,0.2)"),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Actionable Protocol Guidance
    st.markdown("### 📋 Civil Defence & Emergency Action Matrix")
    st.markdown(
        """
| Hazard Vector | Risk Assessment | Operational Action Protocol |
| :--- | :---: | :--- |
| **🌧️ Rainfall** | Low (< 30%) | Standard drainage monitoring; no traffic restrictions. |
| **⛈️ Thunderstorm** | Low (< 30%) | Aviation Doppler active; advisory to ground handling. |
| **🌊 Flooding** | Low (< 25%) | Sump pumps on standby; lake discharge telemetry nominal. |
| **🔥 Heatwave** | Low (< 35%) | Hydration advisories; no peak-hour work suspensions. |
| **🌫️ Fog** | Moderate (30-50%) | CAT-I instrument landing system enabled if visibility < 1000m. |
| **🌪️ Dust Storm** | Low (< 20%) | Particulate air filters active in transit hubs. |
| **💨 Strong Wind** | Low (< 25%) | Coastal marine advisories active for small craft. |
"""
    )
