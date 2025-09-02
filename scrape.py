from get_api_data import scrape_api_data
from get_real_data import scrape_park_data
from supabase_client import clean_6_months_old
import datetime

def scrape():
    timestamp = scrape_park_data(mock=False) # get the timestamp for which real data was scraped for
    scrape_api_data(timestamp, mock=False)
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %I:%M:%S %p")
    if dt.weekday() == 3 and 6 <= dt.hour < 7:  # clean up is done on Thursdays between 6AM and 7AM
        clean_6_months_old()

if __name__ == "__main__":
    scrape()