# file to perform backfill if real_data has more data then predicted
# NOTE: only works in the direction mentioned above, code would need to change to backfill real_data instead
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(os.path.abspath(parent_dir))

from supabase_client import read_timestamps_from_supabase
from get_api_data import scrape_api_data

# function that checks dates between random_forest_predictions and real_data gives a list of dates 
def check_dates():
    real_data_timestamps = read_timestamps_from_supabase("real_data")
    predicted_timestamps = read_timestamps_from_supabase("random_forest_predictions")

    # Find dates that are in predicted but not in real_data
    missing_dates = [dt for dt in real_data_timestamps if dt not in predicted_timestamps]
    print("Missing dates:", missing_dates)
    return missing_dates

def perform_backfill(mock):
    missing_dates = check_dates()
    print("STARTING BACKFILL")
    for date in missing_dates:
        print(f"Fetching data for {date}")
        scrape_api_data(date, mock=mock)
    print("BACKFILL COMPLETE")

if __name__ == "__main__":
    perform_backfill(mock=True)