import os
import sys
from pathlib import Path

# Add frontend directory and root to sys.path so modules import reliably
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from components.navbar import render_navbar

# Import Page Modules
from pages_content import (
    user_dashboard,
    user_weather,
    user_hazards,
    user_map,
    user_reports,
    user_analytics,
    user_profile,
    admin_dashboard,
    admin_weather_data,
    admin_hazards_data,
    admin_reports_data,
    admin_pipelines,
    admin_health
)

# Configure Streamlit App
st.set_page_config(
    page_title="National Weather Big Data Analytics Platform | SIH 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Modern CSS Theme
st.markdown(
    """
    <style>
        /* Base Background and Typography */
        .stApp {
            background-color: #0b1120;
            color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0f172a;
            border-right: 1px solid rgba(71, 85, 105, 0.3);
        }

        /* Metric styling */
        div[data-testid="stMetricValue"] {
            font-size: 26px !important;
            font-weight: 700 !important;
            color: #38bdf8 !important;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            border: none;
        }
        .stButton>button:hover {
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
            transform: translateY(-1px);
        }

        /* Selectboxes and inputs */
        .stSelectbox>div>div, .stTextInput>div>div {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border-color: rgba(71, 85, 105, 0.5) !important;
            border-radius: 8px !important;
        }

        /* Card Container Styling */
        .weather-card {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(71, 85, 105, 0.4);
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }

        /* Table Styling */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(71, 85, 105, 0.3);
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(30, 41, 59, 0.5);
            border-radius: 8px 8px 0 0;
            padding: 8px 16px;
            color: #94a3b8;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(59, 130, 246, 0.2) !important;
            color: #38bdf8 !important;
            border-bottom: 2px solid #38bdf8 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Session State
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "user"
if "is_admin_authenticated" not in st.session_state:
    st.session_state["is_admin_authenticated"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Dashboard"

# Sidebar Navigation
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; padding: 10px 0 16px 0;">
            <div style="background: #2563eb; color: white; padding: 8px; border-radius: 8px; font-size: 20px; font-weight: 800;">
                ⚡
            </div>
            <div>
                <div style="font-weight: 800; font-size: 15px; color: #f8fafc; letter-spacing: -0.3px;">
                    WEATHER ANALYTICS
                </div>
                <div style="font-size: 11px; color: #38bdf8; font-weight: 600;">
                    SIH 2026 • PLATFORM
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Role Selector & Authentication Section
    st.markdown("##### 🔐 Role Access Control")
    selected_role = st.radio(
        "Select Active Role:",
        ["👤 Normal User", "🛡️ Admin Panel"],
        index=0 if st.session_state["user_role"] == "user" else 1,
        key="role_radio"
    )

    if "Admin" in selected_role:
        if not st.session_state["is_admin_authenticated"]:
            st.warning("Admin authentication required.")
            admin_pwd = st.text_input("Enter Admin Passcode:", type="password", key="admin_pwd_input")
            if st.button("Authenticate Admin", use_container_width=True):
                # Passcode check (default: admin2026 or from env)
                valid_pwd = os.environ.get("ADMIN_PASSWORD", "admin2026")
                if admin_pwd == valid_pwd:
                    st.session_state["is_admin_authenticated"] = True
                    st.session_state["user_role"] = "admin"
                    st.session_state["current_page"] = "📊 Admin Dashboard"
                    st.success("Admin Authenticated!")
                    st.rerun()
                else:
                    st.error("Invalid passcode. Try 'admin2026'")
        else:
            st.session_state["user_role"] = "admin"
            if st.button("🚪 Logout Admin", use_container_width=True):
                st.session_state["is_admin_authenticated"] = False
                st.session_state["user_role"] = "user"
                st.session_state["current_page"] = "🏠 Dashboard"
                st.rerun()
    else:
        st.session_state["user_role"] = "user"

    st.markdown("---")

    # Navigation Menu based on Active Role
    st.markdown("##### 🧭 Navigation")
    
    if st.session_state["user_role"] == "user":
        user_pages = [
            "🏠 Dashboard",
            "🌦️ Live Weather",
            "⚠️ Hazard Predictions",
            "🗺️ Weather Map",
            "📹 Verified Reports",
            "📊 Analytics & Alerts",
            "👤 Profile"
        ]
        # Maintain valid page selection
        if st.session_state["current_page"] not in user_pages:
            st.session_state["current_page"] = user_pages[0]

        page_selection = st.radio(
            "Go to Page:",
            user_pages,
            index=user_pages.index(st.session_state["current_page"]) if st.session_state["current_page"] in user_pages else 0,
            key="user_nav_radio"
        )
        st.session_state["current_page"] = page_selection

    else:
        admin_pages = [
            "📊 Admin Dashboard",
            "📋 Weather Data",
            "⚡ Hazard Predictions",
            "🎥 YouTube Reports",
            "🚀 Data Pipelines",
            "🩺 System Health"
        ]
        if st.session_state["current_page"] not in admin_pages:
            st.session_state["current_page"] = admin_pages[0]

        page_selection = st.radio(
            "Go to Admin View:",
            admin_pages,
            index=admin_pages.index(st.session_state["current_page"]) if st.session_state["current_page"] in admin_pages else 0,
            key="admin_nav_radio"
        )
        st.session_state["current_page"] = page_selection

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 11px; color: #64748b; text-align: center; padding-top: 10px;">
            SIH 2026 National Weather Analytics<br/>
            PostgreSQL &bull; Open-Meteo &bull; IMD RMC
        </div>
        """,
        unsafe_allow_html=True
    )

# Render Modern Top Header Navbar
render_navbar()

# Render Selected View
active_page = st.session_state["current_page"]

if st.session_state["user_role"] == "user":
    if active_page == "🏠 Dashboard":
        user_dashboard.render()
    elif active_page == "🌦️ Live Weather":
        user_weather.render()
    elif active_page == "⚠️ Hazard Predictions":
        user_hazards.render()
    elif active_page == "🗺️ Weather Map":
        user_map.render()
    elif active_page == "📹 Verified Reports":
        user_reports.render()
    elif active_page == "📊 Analytics & Alerts":
        user_analytics.render()
    elif active_page == "👤 Profile":
        user_profile.render()

elif st.session_state["user_role"] == "admin" and st.session_state.get("is_admin_authenticated", False):
    if active_page == "📊 Admin Dashboard":
        admin_dashboard.render()
    elif active_page == "📋 Weather Data":
        admin_weather_data.render()
    elif active_page == "⚡ Hazard Predictions":
        admin_hazards_data.render()
    elif active_page == "🎥 YouTube Reports":
        admin_reports_data.render()
    elif active_page == "🚀 Data Pipelines":
        admin_pipelines.render()
    elif active_page == "🩺 System Health":
        admin_health.render()
else:
    st.warning("⚠️ Access Restricted: Please authenticate via the Admin Passcode in the sidebar.")
