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
    if (mock):
        print(f"Mock insert into {table}: {data}")
        return
    print("Successfully wrote data to supabase.")
    supabase.table(table).insert(data).execute()

def read_timestamps_from_supabase(table):
    response = supabase.table(table).select("timestamp").execute()
    response_set = {dt["timestamp"] for dt in response.data}
    return response_set