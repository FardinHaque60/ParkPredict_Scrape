import requests
from bs4 import BeautifulSoup
import re
from supabase_client import write_to_supabase

URL = "https://sjsuparkingstatus.sjsu.edu/"
HEADERS = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request

def fetch_html():
    try:
        response = requests.get(URL, headers=HEADERS, verify=False, timeout=60) 
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

def scrape_park_data(mock=True):
    response_text = fetch_html()

    with open("park_status_pretty.html", "w", encoding="utf-8") as f:
        soup_pretty = BeautifulSoup(response_text, 'html.parser').prettify()
        f.write(soup_pretty)

    if (not response_text):
        print("Error getting response text.")
        return
    
    try:
        soup = BeautifulSoup(response_text, 'html.parser')
        
        # Extract timestamp
        timestamp_element = soup.find("p", class_="timestamp")
        timestamp = None 

        if timestamp_element:
            timestamp_text = timestamp_element.get_text(strip=True, separator=" ")  # Get only text content
            timestamp = timestamp_text.replace("Last updated ", "").replace(" Refresh", "")  # Remove "Last updated" and "Refresh" 
            timestamp = timestamp[:20]
            
            timestamp_pattern = r"^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{2}:\d{2} [APM]{2}$"

            if not re.match(timestamp_pattern, timestamp):  # Ensure expected format
                print(f"Timestamp format is incorrect: {timestamp_text}")
                print(f"stripped version: {timestamp}")
                timestamp = None

        # parse garage fullness data
        garages = []
        for garage in soup.find_all("h2", class_="garage__name"):
            name = garage.text.strip()

            if name == "South Campus Garage":
                break

            fullness_tag = garage.find_next("span", class_="garage__fullness")  # Find fullness relative to name
            fullness = fullness_tag.text.strip().split(" ")[0]  # Get the text content of the fullness tag
            if fullness == "Full":
                fullness = "100"

            try:
                write_to_supabase("real_data", timestamp, name, fullness, mock)
            except Exception as e:
                print(f"Error writing to Supabase: {e}")
            garages.append([timestamp, name, fullness])
        
        print(f"REAL DATA")
        print(f"fetched data for timestamp: {timestamp}.")
        for garage in garages:
            print(f"Garage: {garage[1]}, Fullness: {garage[2]}%")
        print("---------------------------------------")
        return timestamp
    except Exception as e:
        print(f"Error occurred while scraping park data: {e}")

if __name__ == "__main__":
    scrape_park_data()