import streamlit as st
import pandas as pd
from services.supabase_service import get_paginated_weather_records

def render():
    """
    Renders Admin Weather Observations Explorer:
    Searchable, filterable, and paginated view over the 26,000+ database records.
    """
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #dc2626; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 800;">ADMIN</span>
                <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
                    Weather Observations Data Explorer
                </h2>
            </div>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
                Direct SQL query interface to the <code>weather_observations</code> PostgreSQL Supabase table
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Filter & Search Bar
    c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
    with c1:
        search_query = st.text_input("🔍 Search Station or Code:", "", placeholder="e.g. Nungambakkam, Chennai, API")
    with c2:
        source_filter = st.selectbox(
            "Source Filter:",
            ["ALL", "Open-Meteo", "RMC_Chennai_IMD", "Open-Meteo-Archive", "RMC_Chennai_Test"]
        )
    with c3:
        page_size = st.selectbox("Rows per Page:", [10, 25, 50, 100], index=1)
    with c4:
        st.write("")
        st.write("")
        if st.button("Refresh"):
            st.rerun()

    # Session state for page number
    if "admin_weather_page" not in st.session_state:
        st.session_state["admin_weather_page"] = 1

    records, total_count = get_paginated_weather_records(
        page=st.session_state["admin_weather_page"],
        page_size=page_size,
        search_term=search_query,
        source_filter=source_filter
    )

    total_pages = max(1, (total_count + page_size - 1) // page_size)

    # Pagination controls
    p_col1, p_col2, p_col3 = st.columns([2, 4, 2])
    with p_col1:
        if st.button("⬅️ Previous Page", disabled=st.session_state["admin_weather_page"] <= 1):
            st.session_state["admin_weather_page"] -= 1
            st.rerun()
    with p_col2:
        st.markdown(
            f"""
            <div style="text-align: center; padding-top: 6px; font-size: 13px; color: #cbd5e1;">
                Page <strong>{st.session_state['admin_weather_page']}</strong> of <strong>{total_pages:,}</strong> ({total_count:,} total records matching)
            </div>
            """,
            unsafe_allow_html=True
        )
    with p_col3:
        if st.button("Next Page ➡️", disabled=st.session_state["admin_weather_page"] >= total_pages):
            st.session_state["admin_weather_page"] += 1
            st.rerun()

    if records:
        df = pd.DataFrame(records)
        cols_to_show = [c for c in [
            "id", "station_name", "temperature_c", "humidity_percent",
            "wind_speed_kmph", "wind_direction", "pressure_hpa", "rainfall_24h_mm",
            "source", "weather_code", "observation_time", "retrieved_at"
        ] if c in df.columns]
        
        st.dataframe(df[cols_to_show], use_container_width=True, hide_index=True)

        # CSV Export
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Current Page CSV",
            data=csv_data,
            file_name=f"weather_observations_page_{st.session_state['admin_weather_page']}.csv",
            mime="text/csv"
        )
    else:
        st.info("No records match the current search query.")
