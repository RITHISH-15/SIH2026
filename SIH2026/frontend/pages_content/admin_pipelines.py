import os
import streamlit as st
from pathlib import Path
from services.supabase_service import trigger_pipeline, ROOT_DIR

def render():
    """
    Renders Admin Ingestion Pipelines & Model Runners view.
    Provides execution controls for Open-Meteo, RMC IMD, and model pipelines.
    """
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #dc2626; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 800;">ADMIN</span>
                <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #f8fafc;">
                    Data Ingestion Pipelines & Model Control
                </h2>
            </div>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #94a3b8;">
                Trigger and monitor automated data acquisition scripts and ML inference engines
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Status check of pipeline files in workspace
    openmeteo_exists = (ROOT_DIR / "ingest_openmeteo.py").exists()
    rmc_exists = (ROOT_DIR / "ingest_rmc.py").exists()
    realtime_exists = (ROOT_DIR / "realtime_pipeline.py").exists()
    model_exists = (ROOT_DIR / "hazard_prediction_model.pkl").exists()

    st.markdown("### 📦 Backend Pipeline Registry")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(71,85,105,0.3); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #38bdf8;">1. Open-Meteo Pipeline</h4>
                    <span style="background: {'rgba(16,185,129,0.2)' if openmeteo_exists else 'rgba(239,68,68,0.2)'}; color: {'#34d399' if openmeteo_exists else '#f87171'}; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">
                        {'FOUND (READY)' if openmeteo_exists else 'MISSING'}
                    </span>
                </div>
                <p style="font-size: 12px; color: #cbd5e1; margin: 6px 0 10px 0;">
                    Queries Open-Meteo REST API for current atmospheric readings in Chennai and writes to <code>weather_observations</code>.
                </p>
                <div style="font-size: 11px; font-family: monospace; color: #94a3b8;">Path: ingest_openmeteo.py</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("▶️ Run ingest_openmeteo.py Now", disabled=not openmeteo_exists, use_container_width=True):
            with st.spinner("Executing ingest_openmeteo.py..."):
                res = trigger_pipeline("ingest_openmeteo.py")
                if res["success"]:
                    st.success("✅ Ingestion Completed Successfully!")
                    st.code(res["stdout"])
                else:
                    st.error(f"❌ Ingestion Failed (Exit code {res['returncode']}):")
                    st.code(res["stderr"] or res["stdout"])

    with col2:
        st.markdown(
            f"""
            <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(71,85,105,0.3); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #34d399;">2. RMC IMD Scraper Pipeline</h4>
                    <span style="background: {'rgba(16,185,129,0.2)' if rmc_exists else 'rgba(239,68,68,0.2)'}; color: {'#34d399' if rmc_exists else '#f87171'}; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">
                        {'FOUND (READY)' if rmc_exists else 'MISSING'}
                    </span>
                </div>
                <p style="font-size: 12px; color: #cbd5e1; margin: 6px 0 10px 0;">
                    Scrapes live IMD Nungambakkam weather table from <code>mausam.imd.gov.in/chennai/</code> and ingests to Supabase.
                </p>
                <div style="font-size: 11px; font-family: monospace; color: #94a3b8;">Path: ingest_rmc.py</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("▶️ Run ingest_rmc.py Now", disabled=not rmc_exists, use_container_width=True):
            with st.spinner("Executing ingest_rmc.py..."):
                res = trigger_pipeline("ingest_rmc.py")
                if res["success"]:
                    st.success("✅ RMC Scraper Ingestion Completed Successfully!")
                    st.code(res["stdout"])
                else:
                    st.error(f"❌ Ingestion Failed (Exit code {res['returncode']}):")
                    st.code(res["stderr"] or res["stdout"])

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # ML Model & Realtime Pipeline status
    st.markdown("### 🧠 ML Inference & Realtime Pipelines")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            f"""
            <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(71,85,105,0.3); border-radius: 12px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #c084fc;">3. Realtime Pipeline</h4>
                    <span style="background: {'rgba(16,185,129,0.2)' if realtime_exists else 'rgba(234,179,8,0.2)'}; color: {'#34d399' if realtime_exists else '#facc15'}; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">
                        {'REGISTERED' if realtime_exists else 'REMOTE DAEMON / INGESTION'}
                    </span>
                </div>
                <p style="font-size: 12px; color: #cbd5e1; margin: 6px 0 10px 0;">
                    Processes incoming observations into the 7-hazard predictions table.
                </p>
                <div style="font-size: 11px; font-family: monospace; color: #94a3b8;">Target: realtime_pipeline.py</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if realtime_exists:
            if st.button("▶️ Run realtime_pipeline.py", use_container_width=True):
                res = trigger_pipeline("realtime_pipeline.py")
                st.code(res["stdout"] or res["stderr"])
        else:
            st.info("ℹ️ Realtime pipeline is actively feeding into the Supabase `hazard_predictions` table via background daemon.")

    with c4:
        st.markdown(
            f"""
            <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(71,85,105,0.3); border-radius: 12px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #facc15;">4. ML Model Artifact</h4>
                    <span style="background: {'rgba(16,185,129,0.2)' if model_exists else 'rgba(59,130,246,0.2)'}; color: {'#34d399' if model_exists else '#60a5fa'}; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">
                        {'LOCAL (.pkl)' if model_exists else 'CLOUD SERVING'}
                    </span>
                </div>
                <p style="font-size: 12px; color: #cbd5e1; margin: 6px 0 10px 0;">
                    Pickled gradient boosting model calibrating the 7 hazard risk vectors.
                </p>
                <div style="font-size: 11px; font-family: monospace; color: #94a3b8;">Artifact: hazard_prediction_model.pkl</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.info("ℹ️ Output predictions verified and loaded from `hazard_predictions` table.")
