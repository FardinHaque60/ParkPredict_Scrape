import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SECRET_KEY")

# Initialize client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

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

# writes whatever data is passed into method
def write_temp(table, item):
    supabase.table(table).insert(item).execute()
    print("Successfully wrote data to supabase.")