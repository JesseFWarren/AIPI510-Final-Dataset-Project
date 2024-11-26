import pandas as pd

file_path = "traffic_data.csv"
df = pd.read_csv(file_path)

df['distance_km'] = df['distance'].str.replace(',', '').str.replace(' km', '').astype(float)

def consistent_duration(duration_str):
    """
    Ensure duration units are consistent
    """
    if pd.isnull(duration_str):
        return None
    return (
        duration_str.replace("mins", "min")
        .replace("hrs", "hour")
        .replace("s ", " ")
        .replace(" hc", " hours")
        .strip()
    )

df['duration'] = df['duration'].apply(consistent_duration)
df['duration_in_traffic'] = df['duration_in_traffic'].apply(consistent_duration)

def convert_to_minutes(duration_str):
    """
    Convert duration to minutes for visualization
    """
    if pd.isnull(duration_str):
        return None
    days, hours, minutes = 0, 0, 0

    if "day" in duration_str:
        days = int(duration_str.split(" day")[0])
        duration_str = duration_str.split(" day")[1].strip()
    if "hour" in duration_str:
        hours = int(duration_str.split(" hour")[0])
        duration_str = duration_str.split(" hour")[1].strip()
    if "min" in duration_str:
        minutes = int(duration_str.split(" min")[0])

    return days * 24 * 60 + hours * 60 + minutes

df['duration_minutes'] = df['duration'].apply(convert_to_minutes)
df['duration_in_traffic_minutes'] = df['duration_in_traffic'].apply(convert_to_minutes)

df['traffic_difference'] = (
    (df['duration_in_traffic_minutes'] - df['duration_minutes'])
    / df['duration_minutes'] * 100
)

df['average_speed_kph'] = (
    df['distance_km'] / (df['duration_in_traffic_minutes'] / 60)
)

df['traffic_delay_factor'] = (
    (df['duration_in_traffic_minutes'] - df['duration_minutes'])
    / df['distance_km']
)

def classify_traffic_level(percent_time):
    if pd.isnull(percent_time) or percent_time < 0:
        return "Faster"
    elif percent_time == 0:
        return "Same"
    elif percent_time > 0:
        return "Slower"

df['traffic_adjusted'] = df['traffic_difference'].apply(classify_traffic_level)

df.to_csv("traffic_data_with_features.csv", index=False)

print("Features added and dataset saved as 'traffic_data_with_features.csv'.")