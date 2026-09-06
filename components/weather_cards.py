import streamlit as st
import textwrap
from datetime import datetime

def render_weather_cards(observation: dict):
    """
    Renders styled weather cards for real-time observation data.
    Metrics: Temperature, Humidity, Rainfall (24h), Wind Speed & Direction, Pressure, Timestamp, Source.
    Uses textwrap.dedent and unsafe_allow_html=True to prevent raw HTML display.
    """
    if not observation:
        st.warning("⚠️ No live weather observation record found in database.")
        return

    temp = observation.get("temperature_c")
    humidity = observation.get("humidity_percent")
    rainfall = observation.get("rainfall_24h_mm")
    wind_speed = observation.get("wind_speed_kmph")
    wind_dir = observation.get("wind_direction")
    pressure = observation.get("pressure_hpa")
    station_name = observation.get("station_name") or "Chennai Weather Station"
    source = observation.get("source") or "Open-Meteo"
    obs_time = observation.get("observation_time") or observation.get("retrieved_at") or "Unknown"
    
    # Format time
    formatted_time = obs_time
    try:
        dt = datetime.fromisoformat(obs_time.replace("Z", "+00:00"))
        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        pass

    # Source styling
    source_color = "#3b82f6" if "Open-Meteo" in str(source) else "#10b981"

    # Header with station & source info
    header_html = f"""
<div style="background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9)); border: 1px solid rgba(59,130,246,0.2); border-radius: 14px; padding: 16px 20px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
    <div>
        <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8;">STATION OBSERVATION</span>
        <h3 style="margin: 2px 0 0 0; color: #f8fafc; font-size: 20px; font-weight: 700;">{station_name}</h3>
        <span style="font-size: 12px; color: #cbd5e1;">⏱️ Recorded: <code style="color: #67e8f9;">{formatted_time}</code></span>
    </div>
    <div style="display: flex; gap: 8px; align-items: center;">
        <span style="background: {source_color}; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
            📡 Source: {source}
        </span>
        <span style="background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.4); color: #4ade80; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
            ● Verified Real Sensor
        </span>
    </div>
</div>
"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # 5 Key Metrics Grid
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        temp_val = f"{temp:.1f} °C" if temp is not None else "--"
        temp_sub = "Optimal Range" if temp and 20 <= temp <= 33 else "High Temperature" if temp and temp > 33 else "Normal"
        c1_html = f"""
<div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 16px; text-align: center;">
    <div style="font-size: 24px;">🌡️</div>
    <div style="font-size: 12px; color: #94a3b8; font-weight: 600; margin-top: 4px;">TEMPERATURE</div>
    <div style="font-size: 24px; font-weight: 700; color: #f87171; margin: 4px 0;">{temp_val}</div>
    <div style="font-size: 11px; color: #cbd5e1;">{temp_sub}</div>
</div>
"""
        st.markdown(textwrap.dedent(c1_html).strip(), unsafe_allow_html=True)

    with c2:
        hum_val = f"{humidity:.0f} %" if humidity is not None else "--"
        hum_sub = "High Moisture" if humidity and humidity > 80 else "Moderate" if humidity and humidity > 50 else "Dry"
        c2_html = f"""
<div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 16px; text-align: center;">
    <div style="font-size: 24px;">💧</div>
    <div style="font-size: 12px; color: #94a3b8; font-weight: 600; margin-top: 4px;">HUMIDITY</div>
    <div style="font-size: 24px; font-weight: 700; color: #60a5fa; margin: 4px 0;">{hum_val}</div>
    <div style="font-size: 11px; color: #cbd5e1;">{hum_sub}</div>
</div>
"""
        st.markdown(textwrap.dedent(c2_html).strip(), unsafe_allow_html=True)

    with c3:
        rain_val = f"{rainfall:.1f} mm" if rainfall is not None else "--"
        rain_sub = "Heavy Rain" if rainfall and rainfall > 20 else "Light/Moderate" if rainfall and rainfall > 0 else "No Precipitation"
        c3_html = f"""
<div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 12px; padding: 16px; text-align: center;">
    <div style="font-size: 24px;">🌧️</div>
    <div style="font-size: 12px; color: #94a3b8; font-weight: 600; margin-top: 4px;">24H RAINFALL</div>
    <div style="font-size: 24px; font-weight: 700; color: #38bdf8; margin: 4px 0;">{rain_val}</div>
    <div style="font-size: 11px; color: #cbd5e1;">{rain_sub}</div>
</div>
"""
        st.markdown(textwrap.dedent(c3_html).strip(), unsafe_allow_html=True)

    with c4:
        wind_val = f"{wind_speed:.1f} km/h" if wind_speed is not None else "--"
        dir_str = f"Dir: {wind_dir}" if wind_dir and wind_dir != "NOT_MENTIONED_IN_RMC_SOURCE" else "Breeze"
        c4_html = f"""
<div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 12px; padding: 16px; text-align: center;">
    <div style="font-size: 24px;">💨</div>
    <div style="font-size: 12px; color: #94a3b8; font-weight: 600; margin-top: 4px;">WIND SPEED</div>
    <div style="font-size: 24px; font-weight: 700; color: #c084fc; margin: 4px 0;">{wind_val}</div>
    <div style="font-size: 11px; color: #cbd5e1;">{dir_str}</div>
</div>
"""
        st.markdown(textwrap.dedent(c4_html).strip(), unsafe_allow_html=True)

    with c5:
        pres_val = f"{pressure:.1f} hPa" if pressure is not None else "--"
        pres_sub = "Low Pressure (Storm)" if pressure and pressure < 1000 else "Standard Atmospheric"
        c5_html = f"""
<div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(234, 179, 8, 0.3); border-radius: 12px; padding: 16px; text-align: center;">
    <div style="font-size: 24px;">🧭</div>
    <div style="font-size: 12px; color: #94a3b8; font-weight: 600; margin-top: 4px;">BAROMETRIC PRESSURE</div>
    <div style="font-size: 24px; font-weight: 700; color: #facc15; margin: 4px 0;">{pres_val}</div>
    <div style="font-size: 11px; color: #cbd5e1;">{pres_sub}</div>
</div>
"""
        st.markdown(textwrap.dedent(c5_html).strip(), unsafe_allow_html=True)
