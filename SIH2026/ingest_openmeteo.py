import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file!")

supabase: Client = create_client(url, key)

def fetch_and_store_openmeteo():
    # Chennai Coordinates
    latitude = 13.0827
    longitude = 80.2707
    
    # Open-Meteo REST API endpoint for current weather conditions
    api_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&"
        f"current=temperature_2m,relative_humidity_2m,surface_pressure,"
        f"wind_speed_10m,wind_direction_10m,precipitation"
    )
    
    print(f"[INFO] Fetching live data from Open-Meteo API for Chennai ({latitude}, {longitude})...")
    
    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[ERROR] Failed to retrieve Open-Meteo data: {e}")
        return

    current = data.get("current", {})

    # Convert Open-Meteo time (ISO string) to proper timestamp or None
    obs_time_raw = current.get("time")
    obs_time = f"{obs_time_raw}:00Z" if obs_time_raw else None

    # Payload explicitly structured to match your existing weather_observations table
    observation = {
        "station_id": "OPENMETEO_CHENNAI",
        "station_name": "Chennai (Open-Meteo Grid)",
        "observation_time": obs_time,
        "source": "Open-Meteo",
        "source_url": api_url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "temperature_c": current.get("temperature_2m"),
        "humidity_percent": current.get("relative_humidity_2m"),
        "wind_speed_kmph": current.get("wind_speed_10m"),
        "wind_direction": str(current.get("wind_direction_10m")) if current.get("wind_direction_10m") is not None else None,
        "pressure_hpa": current.get("surface_pressure"),
        "rainfall_24h_mm": current.get("precipitation"),
        "weather_code": "OPENMETEO_API"
    }

    print("[INFO] Storing Open-Meteo observation into Supabase...")
    db_response = supabase.table("weather_observations").insert(observation).execute()
    print("[SUCCESS] Open-Meteo record inserted successfully:")
    print(db_response.data)

if __name__ == "__main__":
    fetch_and_store_openmeteo()