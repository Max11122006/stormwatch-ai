import requests
import time
import csv
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
LAT, LON = 52.9, 23.5

def fetch_chunk(start_ts, end_ts):
    url = (
        f"http://history.openweathermap.org/data/2.5/history/city?"
        f"lat={LAT}&lon={LON}&start={start_ts}&end={end_ts}&appid={API_KEY}&units=metric"
    )
    response = requests.get(url)
    if response.status_code != 200:
        print(f"API error: {response.status_code} - {response.text}")
        return []
    return response.json().get('list', [])

def main():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)

    current_start = start_date
    all_data = []

    while current_start < end_date:
        current_end = min(current_start + timedelta(days=5), end_date)
        print(f"Fetching data from {current_start} to {current_end}...")

        start_ts = int(current_start.timestamp())
        end_ts = int(current_end.timestamp())

        data_chunk = fetch_chunk(start_ts, end_ts)
        all_data.extend(data_chunk)

        # Avoid hammering API (be nice)
        time.sleep(1)  

        current_start = current_end

    # Write to CSV
    with open('weather_history_month.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'temp', 'pressure', 'humidity', 'wind_speed', 'weather_code'])

        for item in all_data:
            writer.writerow([
                item['dt'],
                item['main']['temp'],
                item['main']['pressure'],
                item['main']['humidity'],
                item['wind']['speed'],
                item['weather'][0]['id']
            ])

    print(f"Saved {len(all_data)} records to weather_history_month.csv")

if __name__ == "__main__":
    main()