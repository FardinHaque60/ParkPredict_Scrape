import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load .env file
load_dotenv()

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SECRET_KEY")

# Initialize client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def read_south_campus_by_id(id):
    response = supabase.table("actual_south_campus").select("*").eq("id", id).execute()
    if response.data:
        return response.data[0]
    return None

def write_to_supabase(table, timestamp, garage, fullness, mock):
    data = {
        "timestamp": timestamp,
        "garage": garage,
        "fullness": fullness,
    }
    if mock:
        print(f"Mock upsert into {table}: {data}")
        return
    # Check if entry exists
    response = supabase.table(table).select("*").eq("timestamp", timestamp).eq("garage", garage).execute()
    if response.data:
        # Update existing entry
        supabase.table(table).update(data).eq("timestamp", timestamp).eq("garage", garage).execute()
        print("Successfully updated data in supabase.")
    else:
        # Insert new entry
        supabase.table(table).insert(data).execute()
        print("Successfully wrote data to supabase.")

def read_timestamps_from_supabase(table):
    response = supabase.table(table).select("timestamp").execute()
    response_set = {dt["timestamp"] for dt in response.data}
    return response_set

def write_to_actual_south_campus(timestamp, fullness):
    data = {
        "timestamp": timestamp,
        "fullness": fullness,
    }
    response = supabase.table("actual_south_campus").insert(data).execute()
    print("Successfully wrote actual south campus data to supabase.")
    return response.data[0]  # Return the inserted entry

def write_south_campus_people_prediction(timestamp, people):
    data = {
        "timestamp": timestamp,
        "people": people,
    }
    supabase.table("people_prediction_south_campus").insert(data).execute()
    print("Successfully wrote people prediction data to supabase.")

# writes whatever data is passed into method
def write_temp(table, item):
    supabase.table(table).insert(item).execute()
    print("Successfully wrote data to supabase.")

def clean_6_months_old():
    print("CLEANUP")
    tables = ["real_data", "random_forest_predictions", "actual_south_campus", "people_prediction_south_campus"]
    six_months_ago = datetime.now() - timedelta(days=6*30)
    iso_six_months_ago = six_months_ago.isoformat()

    for table in tables:
        response = supabase.table(table).delete().lt("created_at", iso_six_months_ago).execute()
        num_deleted = len(response.data)
        print(f"Number of entries deleted from {table}: {num_deleted}")