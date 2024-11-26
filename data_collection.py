import requests
import pandas as pd
import os
import time
import schedule
import datetime

API_KEY = "AIzaSyBarF1mAOWC0UyxOTfSw95qcvobcXUwKvo"

# 50 largest US cities
origin = "Durham, North Carolina"
destinations = [
    "New York, New York", "Los Angeles, California", "Chicago, Illinois",
    "Houston, Texas", "Phoenix, Arizona", "Philadelphia, Pennsylvania",
    "San Antonio, Texas", "San Diego, California", "Dallas, Texas",
    "San Jose, California", "Austin, Texas", "Jacksonville, Florida",
    "Fort Worth, Texas", "Columbus, Ohio", "Charlotte, North Carolina",
    "San Francisco, California", "Indianapolis, Indiana", "Seattle, Washington",
    "Denver, Colorado", "Washington, D.C.", "Boston, Massachusetts",
    "El Paso, Texas", "Nashville, Tennessee", "Detroit, Michigan",
    "Oklahoma City, Oklahoma", "Portland, Oregon", "Las Vegas, Nevada",
    "Memphis, Tennessee", "Louisville, Kentucky", "Baltimore, Maryland",
    "Milwaukee, Wisconsin", "Albuquerque, New Mexico", "Tucson, Arizona",
    "Fresno, California", "Mesa, Arizona", "Sacramento, California",
    "Atlanta, Georgia", "Kansas City, Missouri", "Colorado Springs, Colorado",
    "Miami, Florida", "Raleigh, North Carolina", "Omaha, Nebraska",
    "Long Beach, California", "Virginia Beach, Virginia", "Oakland, California",
    "Minneapolis, Minnesota", "Tulsa, Oklahoma", "Tampa, Florida",
    "Arlington, Texas", "New Orleans, Louisiana"
]

# output file
csv_file = "traffic_data.csv"

def get_traffic_data():
    """
    Fetch traffic data for a list of destinations using the Google Distance Matrix API.
    """
    print("Fetching traffic data...")
    traffic_data = []
    for destination in destinations:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": destination,
            "departure_time": "now", 
            "key": API_KEY,
        }
        response = requests.get(url, params=params)

        # error checking
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} for {destination}")
            continue

        data = response.json()

        # extract data
        if "rows" in data:
            element = data["rows"][0]["elements"][0]
            traffic_data.append({
                "origin": origin,
                "destination": destination,
                "distance": element.get("distance", {}).get("text"),
                "duration": element.get("duration", {}).get("text"),
                "duration_in_traffic": element.get("duration_in_traffic", {}).get("text"),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
    return traffic_data


def save_to_csv(data):
    """
    Append the traffic data to the csv output file.
    """
    file_exists = os.path.exists(csv_file)
    df = pd.DataFrame(data)

    if file_exists:
        df.to_csv(csv_file, mode="a", index=False, header=False)
    else:
        df.to_csv(csv_file, mode="w", index=False, header=True)

    print(f"Data saved to {csv_file}")

def scheduled_task():
    """
    Function to run each task in the data pipeline.
    """
    data = get_traffic_data()
    if data:
        save_to_csv(data)
    print("Scheduled task complete.")

# first and last our to collect data
start_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
end_time = datetime.datetime.now().replace(hour=23, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)

# schedule hourly data collection tasks between 12 AM and 11 PM (24 hours)
current_time = start_time
already_scheduled = {}
while current_time <= end_time:
    time_str = current_time.strftime("%H:%M")
    if time_str not in already_scheduled:
        schedule.every().day.at(time_str).do(scheduled_task)
        already_scheduled.add(time_str)
    current_time += datetime.timedelta(hours=1)

# scheduler runs until the last collection task completes
print(f"Starting hourly traffic data collection from {start_time} to {end_time}...")
while datetime.datetime.now() < end_time + datetime.timedelta(hours=1):
    schedule.run_pending()
    time.sleep(1)

print("Data collection complete.")