import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client, Client
import streamlit as st

# Locate root directory and load .env
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
env_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

_client: Client = None

def get_supabase_client() -> Client:
    """Returns a singleton Supabase client instance."""
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env or Streamlit secrets")
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client

# ==========================================
# WEATHER OBSERVATIONS (LIVE & HISTORICAL)
# ==========================================

def get_latest_weather_observation(source: str = None) -> dict:
    """
    Fetches the single latest valid weather observation from Supabase.
    Can filter by source, e.g. 'Open-Meteo' or 'RMC_Chennai_IMD'.
    """
    try:
        client = get_supabase_client()
        query = client.table("weather_observations").select("*")
        if source and source != "ALL":
            query = query.eq("source", source)
        
        # Order by retrieved_at or id descending
        response = query.order("id", desc=True).limit(10).execute()
        if response.data:
            # Pick first row that has meaningful numeric measurements if available
            for row in response.data:
                if row.get("temperature_c") is not None or row.get("humidity_percent") is not None:
                    return row
            return response.data[0]
        return {}
    except Exception as e:
        st.error(f"Error querying weather observations: {e}")
        return {}

def get_recent_weather_observations(limit: int = 10) -> list:
    """Fetches recent weather observations across all stations."""
    try:
        client = get_supabase_client()
        response = client.table("weather_observations").select("*").order("id", desc=True).limit(limit).execute()
        return response.data or []
    except Exception as e:
        st.error(f"Error fetching recent weather observations: {e}")
        return []

def get_weather_history_data(limit: int = 250, source: str = None) -> list:
    """
    Fetches historical weather observation records for plotting trends.
    Uses cached query for performance.
    """
    try:
        client = get_supabase_client()
        query = client.table("weather_observations").select(
            "id, observation_time, retrieved_at, temperature_c, humidity_percent, wind_speed_kmph, pressure_hpa, rainfall_24h_mm, source, station_name"
        )
        if source and source != "ALL":
            query = query.eq("source", source)
        
        response = query.order("id", desc=True).limit(limit).execute()
        return response.data or []
    except Exception as e:
        st.error(f"Error fetching historical weather data: {e}")
        return []

# ==========================================
# 7 HAZARD PREDICTIONS
# ==========================================

def get_latest_hazard_predictions(location: str = "Chennai") -> dict:
    """
    Fetches the latest ML hazard prediction record from hazard_predictions table.
    Guarantees returning structure for exactly 7 hazards:
    1. Rainfall
    2. Thunderstorm
    3. Flooding
    4. Heatwave
    5. Fog
    6. Dust Storm
    7. Strong Wind
    """
    default_hazards = {
        "rainfall": {"risk_level": "LOW", "probability": 0.0},
        "thunderstorm": {"risk_level": "LOW", "probability": 0.0},
        "flooding": {"risk_level": "LOW", "probability": 0.0},
        "heatwave": {"risk_level": "LOW", "probability": 0.0},
        "fog": {"risk_level": "LOW", "probability": 0.0},
        "dust_storm": {"risk_level": "LOW", "probability": 0.0},
        "strong_wind": {"risk_level": "LOW", "probability": 0.0}
    }
    try:
        client = get_supabase_client()
        query = client.table("hazard_predictions").select("*")
        if location:
            query = query.ilike("location", f"%{location}%")
        
        response = query.order("id", desc=True).limit(1).execute()
        if response.data and len(response.data) > 0:
            rec = response.data[0]
            preds = rec.get("predictions") or {}
            # Merge with default 7 hazards to ensure completeness
            merged_preds = {}
            for key in ["rainfall", "thunderstorm", "flooding", "heatwave", "fog", "dust_storm", "strong_wind"]:
                if key in preds:
                    merged_preds[key] = preds[key]
                else:
                    merged_preds[key] = default_hazards[key]
            rec["predictions"] = merged_preds
            return rec
        else:
            return {
                "id": None,
                "location": location,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "predictions": default_hazards,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        st.error(f"Error fetching hazard predictions: {e}")
        return {
            "id": None,
            "location": location,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "predictions": default_hazards,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

def get_all_hazard_predictions(limit: int = 50) -> list:
    """Fetches historical hazard predictions for admin table & audit logs."""
    try:
        client = get_supabase_client()
        response = client.table("hazard_predictions").select("*").order("id", desc=True).limit(limit).execute()
        return response.data or []
    except Exception as e:
        st.error(f"Error querying hazard predictions: {e}")
        return []

# ==========================================
# YOUTUBE & VERIFIED SOCIAL REPORTS
# ==========================================

def get_verified_social_reports(
    status_filter: str = "ALL",
    hazard_filter: str = "ALL",
    limit: int = 50
) -> list:
    """
    Fetches records from verified_social_reports including verification_status,
    verification_confidence, verification_reason, fingerprint (SHA-256 hash), and media_url.
    """
    try:
        client = get_supabase_client()
        query = client.table("verified_social_reports").select("*")
        
        if status_filter and status_filter != "ALL":
            query = query.ilike("verification_status", status_filter)
            
        if hazard_filter and hazard_filter != "ALL":
            query = query.ilike("hazard_category", f"%{hazard_filter}%")
            
        response = query.order("id", desc=True).limit(limit).execute()
        return response.data or []
    except Exception as e:
        st.error(f"Error querying verified social reports: {e}")
        return []

def get_public_youtube_reports(limit: int = 50) -> list:
    """Fetches records from public_youtube_reports."""
    try:
        client = get_supabase_client()
        response = client.table("public_youtube_reports").select("*").order("id", desc=True).limit(limit).execute()
        return response.data or []
    except Exception as e:
        st.error(f"Error querying public youtube reports: {e}")
        return []

# ==========================================
# ADMIN METRICS & SYSTEM HEALTH
# ==========================================

def get_database_statistics() -> dict:
    """
    Aggregates exact record counts and freshness metrics across all 4 database tables.
    """
    stats = {
        "weather_count": 0,
        "hazard_count": 0,
        "youtube_count": 0,
        "verified_count": 0,
        "latest_weather_time": "N/A",
        "latest_hazard_time": "N/A",
        "latest_report_time": "N/A",
        "latest_weather_source": "N/A",
        "db_status": "ONLINE"
    }
    try:
        client = get_supabase_client()
        
        # Weather Observations Count
        w_res = client.table("weather_observations").select("id, retrieved_at, source", count="exact").order("id", desc=True).limit(1).execute()
        stats["weather_count"] = w_res.count or len(w_res.data)
        if w_res.data:
            stats["latest_weather_time"] = w_res.data[0].get("retrieved_at", "N/A")
            stats["latest_weather_source"] = w_res.data[0].get("source", "N/A")
            
        # Hazard Predictions Count
        h_res = client.table("hazard_predictions").select("id, created_at, timestamp", count="exact").order("id", desc=True).limit(1).execute()
        stats["hazard_count"] = h_res.count or len(h_res.data)
        if h_res.data:
            stats["latest_hazard_time"] = h_res.data[0].get("timestamp") or h_res.data[0].get("created_at", "N/A")

        # YouTube Reports Count
        y_res = client.table("public_youtube_reports").select("id, collected_at", count="exact").order("id", desc=True).limit(1).execute()
        stats["youtube_count"] = y_res.count or len(y_res.data)

        # Verified Reports Count
        v_res = client.table("verified_social_reports").select("id, processed_at", count="exact").order("id", desc=True).limit(1).execute()
        stats["verified_count"] = v_res.count or len(v_res.data)
        if v_res.data:
            stats["latest_report_time"] = v_res.data[0].get("processed_at", "N/A")

    except Exception as e:
        stats["db_status"] = f"ERROR: {e}"
        
    return stats

def get_paginated_weather_records(
    page: int = 1,
    page_size: int = 20,
    search_term: str = "",
    source_filter: str = "ALL"
) -> tuple:
    """
    Returns (records, total_count) for the Admin Weather Observations data table.
    """
    try:
        client = get_supabase_client()
        query = client.table("weather_observations").select("*", count="exact")
        
        if source_filter and source_filter != "ALL":
            query = query.eq("source", source_filter)
            
        if search_term:
            query = query.or_(f"station_name.ilike.%{search_term}%,station_id.ilike.%{search_term}%,weather_code.ilike.%{search_term}%")
            
        start = (page - 1) * page_size
        end = start + page_size - 1
        response = query.order("id", desc=True).range(start, end).execute()
        
        return response.data or [], response.count or len(response.data)
    except Exception as e:
        st.error(f"Error fetching paginated weather records: {e}")
        return [], 0

# ==========================================
# INGESTION PIPELINE RUNNER
# ==========================================

def trigger_pipeline(script_name: str) -> dict:
    """
    Executes an existing ingestion pipeline script (e.g. ingest_openmeteo.py, ingest_rmc.py)
    directly via Python subprocess and captures realtime stdout & stderr.
    """
    target_path = ROOT_DIR / script_name
    if not target_path.exists():
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"File '{script_name}' does not exist at {target_path}."
        }
        
    try:
        result = subprocess.run(
            [sys.executable, str(target_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(ROOT_DIR),
            encoding="utf-8",
            errors="replace"
        )
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "returncode": -2,
            "stdout": "",
            "stderr": "Pipeline execution timed out after 60 seconds."
        }
    except Exception as e:
        return {
            "success": False,
            "returncode": -3,
            "stdout": "",
            "stderr": str(e)
        }