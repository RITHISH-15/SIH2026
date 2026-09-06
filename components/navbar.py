import os
import streamlit as st
import textwrap
from datetime import datetime

def render_navbar():
    """
    Renders the modern top navigation bar with platform title, SIH 2026 badge,
    real-time status, active role indicator, and quick role switcher.
    Uses textwrap.dedent and unsafe_allow_html=True to ensure clean rendering.
    """
    current_role = st.session_state.get("user_role", "user")
    
    col1, col2, col3 = st.columns([5, 3, 2])
    
    with col1:
        c1_html = """
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
    <div style="background: linear-gradient(135deg, #0ea5e9, #2563eb); padding: 8px 12px; border-radius: 8px; color: white; font-weight: 800; font-size: 20px; box-shadow: 0 4px 12px rgba(37,99,235,0.3);">
        ⚡ SIH 2026
    </div>
    <div>
        <h2 style="margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.5px; color: #f8fafc;">
            National Weather Big Data Analytics Platform
        </h2>
        <p style="margin: 0; font-size: 12px; color: #94a3b8;">
            Real-Time Multi-Source Ingestion • ML Hazard Prediction • Social Verification
        </p>
    </div>
</div>
"""
        st.markdown(textwrap.dedent(c1_html).strip(), unsafe_allow_html=True)
        
    with col2:
        c2_html = """
<div style="display: flex; align-items: center; justify-content: flex-end; gap: 14px; padding-top: 8px;">
    <div style="display: flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); padding: 5px 12px; border-radius: 20px; font-size: 12px; color: #34d399;">
        <span style="height: 8px; width: 8px; background-color: #10b981; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #10b981;"></span>
        Supabase Live
    </div>
    <div style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); padding: 5px 12px; border-radius: 20px; font-size: 12px; color: #60a5fa;">
        Chennai Grid
    </div>
</div>
"""
        st.markdown(textwrap.dedent(c2_html).strip(), unsafe_allow_html=True)

    with col3:
        if current_role == "admin":
            role_badge = '<span style="background: #dc2626; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">ADMIN</span>'
        else:
            role_badge = '<span style="background: #2563eb; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">USER</span>'

        c3_html = f"""
<div style="text-align: right; padding-top: 8px;">
    <span style="font-size: 12px; color: #94a3b8; margin-right: 6px;">Role:</span>
    {role_badge}
</div>
"""
        st.markdown(textwrap.dedent(c3_html).strip(), unsafe_allow_html=True)

    st.markdown("<hr style='margin-top: 4px; margin-bottom: 16px; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)
