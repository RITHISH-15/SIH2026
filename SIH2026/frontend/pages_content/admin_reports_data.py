import streamlit as st
import pandas as pd
from services.supabase_service import get_verified_social_reports, get_public_youtube_reports

def render():
    """
    Renders Admin YouTube Reports & SHA-256 Verification Auditing view.
    """
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #dc2626; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 800;">ADMIN</span>
                <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
                    Multimodal Reports & SHA-256 Deduplication Table
                </h2>
            </div>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
                Cryptographic fingerprinting and cross-sensor corroboration records from <code>verified_social_reports</code>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_verified, tab_youtube = st.tabs(["🛡️ Verified Social Reports (with SHA-256)", "📹 Raw Public YouTube Ingestion"])

    with tab_verified:
        col_status, col_search = st.columns([3, 5])
        with col_status:
            status_filter = st.selectbox(
                "Filter Status:",
                ["ALL", "SUPPORTED", "PARTIALLY_SUPPORTED", "UNVERIFIED", "CONTRADICTED"],
                key="admin_rep_status"
            )
        with col_search:
            search_query = st.text_input("Search Content Text / Fingerprint:", "", key="admin_rep_search")

        reports = get_verified_social_reports(status_filter=status_filter, limit=100)
        
        if search_query:
            reports = [
                r for r in reports if search_query.lower() in str(r.get("content_text", "")).lower() or
                search_query.lower() in str(r.get("fingerprint", "")).lower()
            ]

        if reports:
            df = pd.DataFrame(reports)
            cols_order = [
                "id", "source_type", "hazard_category", "verification_status",
                "verification_confidence", "verification_reason", "fingerprint",
                "extracted_location", "source_url", "processed_at"
            ]
            cols = [c for c in cols_order if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)

            st.download_button(
                "📥 Export Verified Reports CSV",
                df[cols].to_csv(index=False).encode("utf-8"),
                "verified_reports_audit.csv",
                "text/csv"
            )
        else:
            st.info("No verified social reports found matching the criteria.")

    with tab_youtube:
        raw_yt = get_public_youtube_reports(limit=100)
        if raw_yt:
            df_yt = pd.DataFrame(raw_yt)
            cols_yt = [c for c in ["id", "video_id", "title", "channel", "published_at", "collected_at", "video_url"] if c in df_yt.columns]
            st.dataframe(df_yt[cols_yt], use_container_width=True, hide_index=True)
        else:
            st.info("No raw YouTube reports found.")
