import streamlit as st
import textwrap
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_weather_trends_chart(history_data: list):
    """
    Renders interactive multi-metric time series charts from historical weather observations.
    """
    if not history_data:
        st.info("ℹ️ Insufficient historical data for trend analysis.")
        return

    df = pd.DataFrame(history_data)
    
    # Sort chronological
    if "observation_time" in df.columns and df["observation_time"].notna().any():
        df["time"] = pd.to_datetime(df["observation_time"])
    else:
        df["time"] = pd.to_datetime(df["retrieved_at"])
        
    df = df.sort_values("time")

    tab1, tab2, tab3 = st.tabs(["🌡️ Temperature & Humidity", "🌧️ Rainfall & Pressure", "💨 Wind Speed"])

    with tab1:
        fig1 = go.Figure()
        if "temperature_c" in df.columns:
            fig1.add_trace(go.Scatter(
                x=df["time"], y=df["temperature_c"],
                name="Temperature (°C)",
                line=dict(color="#ef4444", width=2.5),
                mode="lines+markers"
            ))
        if "humidity_percent" in df.columns:
            fig1.add_trace(go.Scatter(
                x=df["time"], y=df["humidity_percent"],
                name="Humidity (%)",
                yaxis="y2",
                line=dict(color="#3b82f6", width=2, dash="dot"),
                mode="lines"
            ))
        fig1.update_layout(
            title="Temperature & Humidity Time-Series (Big Data Ingestion)",
            paper_bgcolor="rgba(15,23,42,0)",
            plot_bgcolor="rgba(30,41,59,0.4)",
            font=dict(color="#cbd5e1"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Temperature (°C)", gridcolor="rgba(71,85,105,0.2)"),
            yaxis2=dict(title="Humidity (%)", overlaying="y", side="right", gridcolor="rgba(71,85,105,0.1)"),
            xaxis=dict(gridcolor="rgba(71,85,105,0.2)"),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = go.Figure()
        if "rainfall_24h_mm" in df.columns:
            fig2.add_trace(go.Bar(
                x=df["time"], y=df["rainfall_24h_mm"],
                name="24h Rainfall (mm)",
                marker_color="#0ea5e9"
            ))
        if "pressure_hpa" in df.columns:
            fig2.add_trace(go.Scatter(
                x=df["time"], y=df["pressure_hpa"],
                name="Pressure (hPa)",
                yaxis="y2",
                line=dict(color="#eab308", width=2),
                mode="lines"
            ))
        fig2.update_layout(
            title="Rainfall Accumulation & Barometric Pressure Correlation",
            paper_bgcolor="rgba(15,23,42,0)",
            plot_bgcolor="rgba(30,41,59,0.4)",
            font=dict(color="#cbd5e1"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Rainfall (mm)", gridcolor="rgba(71,85,105,0.2)"),
            yaxis2=dict(title="Pressure (hPa)", overlaying="y", side="right", gridcolor="rgba(71,85,105,0.1)"),
            xaxis=dict(gridcolor="rgba(71,85,105,0.2)"),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        if "wind_speed_kmph" in df.columns:
            fig3 = px.area(
                df, x="time", y="wind_speed_kmph",
                title="Sustained Wind Speed Profile (km/h)",
                color_discrete_sequence=["#a855f7"]
            )
            fig3.update_layout(
                paper_bgcolor="rgba(15,23,42,0)",
                plot_bgcolor="rgba(30,41,59,0.4)",
                font=dict(color="#cbd5e1"),
                xaxis=dict(gridcolor="rgba(71,85,105,0.2)"),
                yaxis=dict(title="Wind Speed (km/h)", gridcolor="rgba(71,85,105,0.2)"),
                margin=dict(l=40, r=40, t=50, b=40)
            )
            st.plotly_chart(fig3, use_container_width=True)

def render_hazard_radar_chart(hazard_record: dict):
    """
    Renders a polar radar chart comparing model probability across the 7 hazards.
    """
    preds = hazard_record.get("predictions", {}) if hazard_record else {}
    labels = ["Rainfall", "Thunderstorm", "Flooding", "Heatwave", "Fog", "Dust Storm", "Strong Wind"]
    keys = ["rainfall", "thunderstorm", "flooding", "heatwave", "fog", "dust_storm", "strong_wind"]
    
    values = []
    for k in keys:
        p = preds.get(k, {}).get("probability", 0.0)
        p_val = p * 100 if p <= 1.0 else p
        values.append(p_val)
        
    # Close radar loop
    r_values = values + [values[0]]
    r_labels = labels + [labels[0]]

    fig = go.Figure(data=go.Scatterpolar(
        r=r_values,
        theta=r_labels,
        fill="toself",
        fillcolor="rgba(14, 165, 233, 0.3)",
        line=dict(color="#0ea5e9", width=2.5),
        marker=dict(size=7, color="#38bdf8")
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(71,85,105,0.3)", color="#94a3b8"),
            angularaxis=dict(gridcolor="rgba(71,85,105,0.3)", color="#f8fafc")
        ),
        paper_bgcolor="rgba(15,23,42,0)",
        font=dict(color="#cbd5e1"),
        title="7-Hazard Probability Radar Spectrum (%)",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_verification_donut_chart(reports: list):
    """
    Renders verification status distribution donut chart.
    """
    if not reports:
        return
        
    statuses = [str(r.get("verification_status") or "UNVERIFIED").upper() for r in reports]
    df = pd.DataFrame({"status": statuses})
    counts = df["status"].value_counts().reset_index()
    counts.columns = ["Status", "Count"]

    color_map = {
        "SUPPORTED": "#10b981",
        "PARTIALLY_SUPPORTED": "#3b82f6",
        "UNVERIFIED": "#f59e0b",
        "CONTRADICTED": "#ef4444"
    }

    fig = px.pie(
        counts,
        names="Status",
        values="Count",
        hole=0.55,
        title="Social Report Verification Status Ratio",
        color="Status",
        color_discrete_map=color_map
    )
    fig.update_layout(
        paper_bgcolor="rgba(15,23,42,0)",
        font=dict(color="#cbd5e1"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=50, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_alert_banner(hazard_record: dict):
    """
    Checks if any of the 7 hazards exceed risk thresholds and displays an alert banner.
    """
    if not hazard_record:
        return
        
    preds = hazard_record.get("predictions", {})
    high_risks = []
    med_risks = []
    
    for name, data in preds.items():
        risk = str(data.get("risk_level", "LOW")).upper()
        prob = float(data.get("probability", 0.0))
        prob_pct = prob * 100 if prob <= 1.0 else prob
        
        if risk == "HIGH" or prob_pct >= 60:
            high_risks.append((name.replace("_", " ").title(), prob_pct))
        elif risk == "MEDIUM" or prob_pct >= 30:
            med_risks.append((name.replace("_", " ").title(), prob_pct))

    if high_risks:
        alerts_str = ", ".join([f"{h[0]} ({h[1]:.0f}%)" for h in high_risks])
        b_html = f"""
<div style="background: rgba(220, 38, 38, 0.25); border: 2px solid #ef4444; border-radius: 10px; padding: 12px 18px; margin-bottom: 18px; display: flex; align-items: center; gap: 12px;">
    <span style="font-size: 28px;">🚨</span>
    <div>
        <h4 style="margin: 0; color: #fca5a5; font-size: 15px; font-weight: 700;">CRITICAL WEATHER HAZARD ALERT</h4>
        <p style="margin: 2px 0 0 0; color: #fee2e2; font-size: 13px;">
            High risk detected for: <strong>{alerts_str}</strong>. Immediate public advisories recommended.
        </p>
    </div>
</div>
"""
        st.markdown(textwrap.dedent(b_html).strip(), unsafe_allow_html=True)
    elif med_risks:
        alerts_str = ", ".join([f"{m[0]} ({m[1]:.0f}%)" for m in med_risks])
        b_html = f"""
<div style="background: rgba(217, 119, 6, 0.2); border: 1px solid #f59e0b; border-radius: 10px; padding: 12px 18px; margin-bottom: 18px; display: flex; align-items: center; gap: 12px;">
    <span style="font-size: 24px;">⚠️</span>
    <div>
        <h4 style="margin: 0; color: #fcd34d; font-size: 14px; font-weight: 700;">WEATHER WATCH ADVISORY</h4>
        <p style="margin: 2px 0 0 0; color: #fef3c7; font-size: 12.5px;">
            Elevated probability observed for: <strong>{alerts_str}</strong>. Continuous radar monitoring in effect.
        </p>
    </div>
</div>
"""
        st.markdown(textwrap.dedent(b_html).strip(), unsafe_allow_html=True)
    else:
        b_html = """
<div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 10px 16px; margin-bottom: 18px; display: flex; align-items: center; gap: 10px;">
    <span style="font-size: 20px;">🛡️</span>
    <span style="color: #6ee7b7; font-size: 13px; font-weight: 600;">
        All 7 ML Hazard Vectors Nominal. No active high-severity weather alerts for Chennai region.
    </span>
</div>
"""
        st.markdown(textwrap.dedent(b_html).strip(), unsafe_allow_html=True)

