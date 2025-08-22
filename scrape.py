from get_api_data import scrape_api_data
from get_real_data import scrape_park_data


def scrape():
    timestamp = scrape_park_data(mock=False) # get the timestamp for which real data was scraped for
    scrape_api_data(timestamp, mock=False)

if __name__ == "__main__":
    scrape()