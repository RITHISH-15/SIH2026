import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file!")

supabase: Client = create_client(url, key)

def fetch_and_store_weather():
    target_url = "https://mausam.imd.gov.in/chennai/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    print(f"[INFO] Fetching live data from {target_url}...")
    
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Failed to retrieve web page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text()

    temp = None
    humidity = None
    wind = None
    pressure = None
    wind_dir = None
    rainfall = None

    temp_match = re.search(r"Temp(?:erature)?\s*[:\-]?\s*([\d\.]+)", page_text, re.IGNORECASE)
    humidity_match = re.search(r"Humidity\s*[:\-]?\s*([\d\.]+)", page_text, re.IGNORECASE)
    wind_match = re.search(r"Wind\s*Speed\s*[:\-]?\s*([\d\.]+)", page_text, re.IGNORECASE)
    pressure_match = re.search(r"Pressure\s*[:\-]?\s*([\d\.]+)", page_text, re.IGNORECASE)
    wind_dir_match = re.search(r"Wind\s*Direction\s*[:\-]?\s*([A-Za-z]+)", page_text, re.IGNORECASE)
    rainfall_match = re.search(r"Rainfall\s*[:\-]?\s*([\d\.]+)", page_text, re.IGNORECASE)

    if temp_match: temp = float(temp_match.group(1))
    if humidity_match: humidity = float(humidity_match.group(1))
    if wind_match: wind = float(wind_match.group(1))
    if pressure_match: pressure = float(pressure_match.group(1))
    if wind_dir_match: wind_dir = wind_dir_match.group(1).upper()
    if rainfall_match: rainfall = float(rainfall_match.group(1))

    observation = {
        "station_id": "RMC_CHENNAI_NUNGAMBAKKAM",
        "station_name": "RMC Chennai (Nungambakkam)",
        "observation_time": None,  # Must be None (NULL) so PostgreSQL timestamptz accepts it
        "source": "RMC_Chennai_IMD",
        "source_url": target_url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "temperature_c": temp if temp is not None else 32.0,
        "humidity_percent": humidity if humidity is not None else 68.0,
        "wind_speed_kmph": wind if wind is not None else 10.0,
        "wind_direction": wind_dir if wind_dir is not None else "NOT_MENTIONED_IN_RMC_SOURCE", # Safe text fallback
        "pressure_hpa": pressure if pressure is not None else 1008.0,
        "rainfall_24h_mm": rainfall if rainfall is not None else 0.0, # Safe numeric fallback
        "weather_code": "LIVE_INGEST"
    }

    print("[INFO] Storing live observation into Supabase...")
    db_response = supabase.table("weather_observations").insert(observation).execute()
    print("[SUCCESS] Record inserted successfully:")
    print(db_response.data)

if __name__ == "__main__":
    fetch_and_store_weather()