import streamlit as st
import textwrap

def render_filter_bar():
    """
    Renders the professional filter bar:
    - Location
    - Radius (1 km, 5 km, 10 km, 25 km)
    - Hazard Category
    - Verification Status
    - Data Source
    Stores selection in st.session_state.
    Uses textwrap.dedent and unsafe_allow_html=True to prevent raw HTML display.
    """
    # Initialize session state filter keys if not present
    if "filter_location" not in st.session_state:
        st.session_state["filter_location"] = "Chennai"
    if "filter_radius_km" not in st.session_state:
        st.session_state["filter_radius_km"] = 10
    if "filter_hazard" not in st.session_state:
        st.session_state["filter_hazard"] = "ALL"
    if "filter_verification" not in st.session_state:
        st.session_state["filter_verification"] = "ALL"
    if "filter_source" not in st.session_state:
        st.session_state["filter_source"] = "ALL"
        
    with st.container():
        bar_html = """
<div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(71, 85, 105, 0.4); border-radius: 12px; padding: 12px 16px; margin-bottom: 20px;">
    <div style="font-weight: 600; font-size: 13px; color: #cbd5e1; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
        <span>🔍 GLOBAL WEATHER & HAZARD FILTERS</span>
    </div>
</div>
"""
        st.markdown(textwrap.dedent(bar_html).strip(), unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 2, 2, 1.5, 1])
        
        with col1:
            location = st.selectbox(
                "📍 Location",
                ["Chennai", "Nungambakkam", "Meenambakkam", "Tambaram", "Guindy", "Custom"],
                index=["Chennai", "Nungambakkam", "Meenambakkam", "Tambaram", "Guindy", "Custom"].index(
                    st.session_state["filter_location"] if st.session_state["filter_location"] in ["Chennai", "Nungambakkam", "Meenambakkam", "Tambaram", "Guindy", "Custom"] else "Chennai"
                ),
                key="sel_location"
            )
            st.session_state["filter_location"] = location

        with col2:
            radius_options = [1, 5, 10, 25]
            radius_val = st.selectbox(
                "⭕ Radius (km)",
                radius_options,
                index=radius_options.index(st.session_state["filter_radius_km"]) if st.session_state["filter_radius_km"] in radius_options else 2,
                format_func=lambda x: f"{x} km",
                key="sel_radius"
            )
            st.session_state["filter_radius_km"] = radius_val

        with col3:
            hazard_options = ["ALL", "Rainfall", "Thunderstorm", "Flooding", "Heatwave", "Fog", "Dust Storm", "Strong Wind"]
            hazard = st.selectbox(
                "⚠️ Hazard",
                hazard_options,
                index=hazard_options.index(st.session_state["filter_hazard"]) if st.session_state["filter_hazard"] in hazard_options else 0,
                key="sel_hazard"
            )
            st.session_state["filter_hazard"] = hazard

        with col4:
            verification_options = ["ALL", "SUPPORTED", "PARTIALLY_SUPPORTED", "UNVERIFIED", "CONTRADICTED"]
            verification = st.selectbox(
                "🛡️ Verification",
                verification_options,
                index=verification_options.index(st.session_state["filter_verification"]) if st.session_state["filter_verification"] in verification_options else 0,
                key="sel_verification"
            )
            st.session_state["filter_verification"] = verification

        with col5:
            source_options = ["ALL", "Open-Meteo", "RMC_Chennai_IMD", "YouTube"]
            source = st.selectbox(
                "📡 Source",
                source_options,
                index=source_options.index(st.session_state["filter_source"]) if st.session_state["filter_source"] in source_options else 0,
                key="sel_source"
            )
            st.session_state["filter_source"] = source

        with col6:
            st.write("")
            st.write("")
            if st.button("🔄 Sync", help="Refresh data from database", use_container_width=True):
                st.rerun()

    return {
        "location": st.session_state["filter_location"],
        "radius_km": st.session_state["filter_radius_km"],
        "hazard": st.session_state["filter_hazard"],
        "verification": st.session_state["filter_verification"],
        "source": st.session_state["filter_source"]
    }
