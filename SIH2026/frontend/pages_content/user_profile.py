import streamlit as st

def render():
    """
    Renders User Preferences, Saved Stations, and Alert Thresholds.
    """
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
                👤 User Profile & Alert Thresholds
            </h2>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
                Configure regional notifications, monitoring preferences, and API telemetry keys
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([5, 5])

    with c1:
        st.markdown(
            """
            <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(71,85,105,0.3); border-radius: 12px; padding: 18px; margin-bottom: 16px;">
                <h4 style="margin: 0 0 12px 0; color: #38bdf8;">Regional Monitoring Preferences</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        def_loc = st.selectbox("Primary Monitoring Zone:", ["Chennai Central", "Nungambakkam", "Meenambakkam", "Tambaram"])
        def_rad = st.slider("Default GIS Impact Radius (km):", 1, 50, 10)
        units = st.radio("Temperature Units:", ["Celsius (°C)", "Fahrenheit (°F)"], horizontal=True)

    with c2:
        st.markdown(
            """
            <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(71,85,105,0.3); border-radius: 12px; padding: 18px; margin-bottom: 16px;">
                <h4 style="margin: 0 0 12px 0; color: #facc15;">Early Warning Notification Triggers</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.checkbox("🚨 Critical Rain Alert (> 50mm / 24h)", value=True)
        st.checkbox("⚡ Thunderstorm Convective Warning", value=True)
        st.checkbox("🌊 Urban Waterlogging Prediction Alert", value=True)
        st.checkbox("💨 High Wind Gust Advisory (> 40 km/h)", value=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button("💾 Save Preferences", use_container_width=False):
        st.success("✅ Preferences saved to local session successfully!")
