import requests
import re
from supabase_client import write_to_supabase
import datetime

URL = "https://parkpredict-api.fly.dev/api/predict?timestamp="
HEADERS = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request

def fetch_api(timestamp, mock=True):
    # Convert timestamp string to ISO format
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %I:%M:%S %p")
    iso_timestamp = dt.isoformat()
    url = URL + iso_timestamp
    try:
        response = requests.get(url, headers=HEADERS, verify=False, timeout=60)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

def scrape_api_data(input_timestamp, mock=True):
    response = fetch_api(input_timestamp)
    timestamp = response.get("timestamp")
    response_data = response.get("predictions")

    if (not response_data):
        print("Error getting response data.")
        return

    garages = []
    for garage in response_data:
        garages.append([input_timestamp, garage, response_data[garage]])

        try:
            write_to_supabase("random_forest_predictions", input_timestamp, garage, response_data[garage], mock)
        except Exception as e:
            print(f"Error writing to Supabase: {e}")

    print(f"RANDOM FOREST DATA")
    print(f"fetched data for timestamp: {timestamp}.")
    for garage in garages:
        print(f"Garage: {garage[1]}, Fullness: {garage[2]}%")
    print("---------------------------------------")

if __name__ == "__main__":
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    scrape_api_data(timestamp)