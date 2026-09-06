import streamlit as st
import textwrap

HAZARD_CONFIG = {
    "rainfall": {
        "title": "Rainfall",
        "icon": "🌧️",
        "description": "Precipitation and heavy downpour probability"
    },
    "thunderstorm": {
        "title": "Thunderstorm",
        "icon": "⛈️",
        "description": "Convective storm, lightning, and thunder activity"
    },
    "flooding": {
        "title": "Flooding",
        "icon": "🌊",
        "description": "Urban waterlogging and drainage overflow risk"
    },
    "heatwave": {
        "title": "Heatwave",
        "icon": "🔥",
        "description": "Extreme surface temperature & high heat index"
    },
    "fog": {
        "title": "Fog",
        "icon": "🌫️",
        "description": "Low surface visibility affecting transport & aviation"
    },
    "dust_storm": {
        "title": "Dust Storm",
        "icon": "🌪️",
        "description": "Suspended particulate matter and high gust events"
    },
    "strong_wind": {
        "title": "Strong Wind",
        "icon": "💨",
        "description": "Gale-force gusts and structural hazard risks"
    }
}

def render_hazard_cards(hazard_record: dict):
    """
    Renders exactly 7 hazard predictions with probability, risk level (LOW, MEDIUM, HIGH),
    and timestamp directly sourced from hazard_predictions ML pipeline.
    Uses st.markdown with unsafe_allow_html=True and textwrap.dedent to ensure custom CSS
    and layout render cleanly without displaying raw HTML tags.
    """
    if not hazard_record:
        st.warning("⚠️ No hazard prediction model output available.")
        return

    predictions = hazard_record.get("predictions", {})
    timestamp = hazard_record.get("timestamp") or hazard_record.get("created_at") or "Recent"
    location = hazard_record.get("location") or "Chennai"

    header_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin: 16px 0 12px 0;">
    <div>
        <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #f8fafc;">
            🎯 7-Hazard ML Operational Risk Matrix
        </h3>
        <p style="margin: 2px 0 0 0; font-size: 12px; color: #94a3b8;">
            Location: <span style="color: #38bdf8; font-weight: 600;">{location}</span> • Model Run: <code>{timestamp}</code>
        </p>
    </div>
    <div style="background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 8px; padding: 4px 10px; font-size: 11px; color: #38bdf8; font-weight: 600;">
        🧠 Pipeline: hazard_prediction_model.pkl
    </div>
</div>
"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # Render in 4 + 3 grid layout
    hazards_order = ["rainfall", "thunderstorm", "flooding", "heatwave", "fog", "dust_storm", "strong_wind"]

    # First row: 4 hazards
    cols_row1 = st.columns(4)
    for i, hazard_key in enumerate(hazards_order[:4]):
        hazard_meta = HAZARD_CONFIG.get(hazard_key, {"title": hazard_key.capitalize(), "icon": "⚠️", "description": ""})
        hazard_data = predictions.get(hazard_key, {"risk_level": "LOW", "probability": 0.0})
        with cols_row1[i]:
            _render_single_hazard(hazard_key, hazard_meta, hazard_data)

    # Second row: 3 hazards centered
    cols_row2 = st.columns([1, 1, 1])
    for i, hazard_key in enumerate(hazards_order[4:]):
        hazard_meta = HAZARD_CONFIG.get(hazard_key, {"title": hazard_key.capitalize(), "icon": "⚠️", "description": ""})
        hazard_data = predictions.get(hazard_key, {"risk_level": "LOW", "probability": 0.0})
        with cols_row2[i]:
            _render_single_hazard(hazard_key, hazard_meta, hazard_data)

def _render_single_hazard(key: str, meta: dict, data: dict):
    risk_level = str(data.get("risk_level", "LOW")).upper()
    prob = float(data.get("probability", 0.0))
    prob_percent = prob * 100 if prob <= 1.0 else prob

    if risk_level == "HIGH" or prob_percent >= 65:
        badge_bg = "rgba(239, 68, 68, 0.2)"
        badge_border = "#ef4444"
        badge_text = "#f87171"
        card_border = "rgba(239, 68, 68, 0.4)"
        advisory = "CRITICAL: Implement emergency readiness protocols."
    elif risk_level == "MEDIUM" or prob_percent >= 30:
        badge_bg = "rgba(245, 158, 11, 0.2)"
        badge_border = "#f59e0b"
        badge_text = "#fbbf24"
        card_border = "rgba(245, 158, 11, 0.4)"
        advisory = "ADVISORY: Monitor regional radar and sensors."
    else:
        badge_bg = "rgba(16, 185, 129, 0.2)"
        badge_border = "#10b981"
        badge_text = "#34d399"
        card_border = "rgba(16, 185, 129, 0.2)"
        advisory = "NOMINAL: Normal conditions expected."

    card_html = f"""
<div style="background: rgba(30, 41, 59, 0.85); border: 1px solid {card_border}; border-radius: 12px; padding: 14px; margin-bottom: 12px;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 24px;">{meta['icon']}</span>
            <div>
                <div style="font-weight: 700; font-size: 15px; color: #f8fafc;">{meta['title']}</div>
                <div style="font-size: 11px; color: #94a3b8;">{meta['description']}</div>
            </div>
        </div>
        <div style="background: {badge_bg}; border: 1px solid {badge_border}; color: {badge_text}; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; letter-spacing: 0.5px;">
            {risk_level}
        </div>
    </div>
    
    <div style="margin: 10px 0 6px 0;">
        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #cbd5e1; margin-bottom: 4px;">
            <span>Model Probability</span>
            <span style="font-weight: 700; color: {badge_text};">{prob_percent:.1f}%</span>
        </div>
        <div style="background: rgba(15, 23, 42, 0.6); border-radius: 6px; height: 8px; overflow: hidden;">
            <div style="background: {badge_border}; width: {min(max(prob_percent, 4), 100)}%; height: 100%; border-radius: 6px;"></div>
        </div>
    </div>

    <div style="font-size: 10.5px; color: #94a3b8; border-top: 1px solid rgba(148,163,184,0.1); padding-top: 6px; margin-top: 6px;">
        {advisory}
    </div>
</div>
"""
    st.markdown(textwrap.dedent(card_html).strip(), unsafe_allow_html=True)
