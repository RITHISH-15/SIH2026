import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timezone

# Load variables from .env
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file!")

# Initialize Supabase client
supabase: Client = create_client(url, key)

print("[INFO] Connecting to Supabase...")

# Test record including required NOT NULL fields
test_data = {
    "station_name": "RMC Chennai Central",
    "source": "RMC_Chennai_Test",
    "retrieved_at": datetime.now(timezone.utc).isoformat()
}

# 1. Test INSERT
print("[INFO] Inserting test record...")
insert_response = supabase.table("weather_observations").insert(test_data).execute()
print("[SUCCESS] Inserted row:", insert_response.data)

# 2. Test SELECT
print("[INFO] Querying weather_observations table...")
select_response = supabase.table("weather_observations").select("*").execute()
print(f"[SUCCESS] Retrieved {len(select_response.data)} row(s) from database.")
print("Database schema structure:", select_response.data[0] if select_response.data else "No records found")