import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
import plotly.express as px
from geopy.geocoders import Nominatim
import requests
from geopy.geocoders import GoogleV3
from geopy.exc import GeopyError

file_path = "traffic_data_with_features.csv"
df = pd.read_csv(file_path)

df = df.iloc[1:].reset_index(drop=True)

def standardize_timestamp_format(timestamp_str):
    """
    Function to standardize the timestamps
    """
    if pd.isnull(timestamp_str):
        return None  
    if re.match(r"^\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}$", timestamp_str):
        return timestamp_str
    try:
        return pd.to_datetime(timestamp_str).strftime("%m/%d/%Y %H:%M")
    except Exception:
        return None

df['timestamp'] = df['timestamp'].apply(standardize_timestamp_format)

df['timestamp'] = pd.to_datetime(df['timestamp'], format="%m/%d/%Y %H:%M", errors='coerce')

df['hour'] = df['timestamp'].dt.hour

def convert_to_minutes(duration_str):
    """
    convert duration to minutes format
    """
    if pd.isnull(duration_str):
        return None 
    days, hours, minutes = 0, 0, 0

    day_match = re.search(r'(\d+) day', duration_str)
    hour_match = re.search(r'(\d+) hour', duration_str)
    minute_match = re.search(r'(\d+) min', duration_str)

    if day_match:
        days = int(day_match.group(1))
    if hour_match:
        hours = int(hour_match.group(1))
    if minute_match:
        minutes = int(minute_match.group(1))

    return days * 24 * 60 + hours * 60 + minutes

df['duration'] = df['duration'].apply(convert_to_minutes)
df['duration_in_traffic'] = df['duration_in_traffic'].apply(convert_to_minutes)

df['duration_in_traffic'] = df['duration_in_traffic'].fillna(df['duration'])

avg_duration = df.groupby('hour')['duration_in_traffic'].mean()

plt.scatter(df['distance'], df['duration'], alpha=0.6)
plt.title('Distance vs. Duration')
plt.xlabel('Distance (km)')
plt.ylabel('Duration (minutes)')

plt.xticks(rotation=45)  
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))

plt.grid()
plt.show()

df = df[df['duration_in_traffic'].notna()]
df = df[df['duration_in_traffic'] > 0]

avg_duration = df.groupby('hour')['traffic_difference'].mean()

plt.plot(avg_duration.index, avg_duration.values, marker='o')
plt.title('Average Travel Time Percent Difference Acounting For Traffic')
plt.xlabel('Hour of Day')
plt.ylabel('Percent Time Difference')
plt.grid()
plt.show()

avg_percent_traffic_dest = df.groupby('destination')['traffic_difference'].mean().sort_values()

avg_percent_traffic_dest.plot(kind='barh', figsize=(10, 8))
plt.title('Average Travel Time Percent Difference Acounting For Traffic by Destination')
plt.xlabel('Percent Time Difference')
plt.ylabel('Destination')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

print("Preparing US Map Visualization...")
geolocator = GoogleV3(api_key="AIzaSyBarF1mAOWC0UyxOTfSw95qcvobcXUwKvo")

def get_coordinates(destination):
    """
    Fetch location coordinates from google api
    """
    try:
        location = geolocator.geocode(destination, timeout=5)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"No results found for {destination}.")
            return None, None
    except GeopyError as e:
        print(f"Error fetching coordinates for {destination}: {e}")
        return None, None

df['latitude'], df['longitude'] = zip(*df['destination'].apply(get_coordinates))

df.dropna(subset=['latitude', 'longitude', 'traffic_difference'], inplace=True)

average_df = df.groupby('destination', as_index=False).agg(
    avg_traffic_difference=('traffic_difference', 'mean'),
    latitude=('latitude', 'first'),
    longitude=('longitude', 'first')
)

average_df['size_scaled'] = (
    average_df['avg_traffic_difference'] - average_df['avg_traffic_difference'].min() + 1
)

fig = px.scatter_geo(
    average_df,
    lat='latitude',
    lon='longitude',
    text='destination',
    size='size_scaled',  
    color='avg_traffic_difference',
    color_continuous_scale='RdBu',
    title='Average Traffic Difference by Destination',
    labels={'avg_traffic_difference': 'Avg Traffic Difference (mins)'}
)

fig.update_layout(
    geo=dict(
        scope='usa',
        showland=True,
        landcolor="rgb(243, 243, 243)",
        subunitcolor="rgb(217, 217, 217)",
    ),
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
)

fig.update_traces(
    textposition="top center",
    hovertemplate="<b>%{text}</b><br>Avg Traffic Difference: %{marker.color:.2f} mins"
)

fig.show()


heatmap_data = df.pivot_table(
    index='destination',
    columns='hour',
    values='traffic_difference',
    aggfunc='mean'
)

plt.figure(figsize=(24, 16))
sns.heatmap(heatmap_data, cmap='YlOrRd', annot=False)
plt.title('Traffic Duration Heatmap')
plt.xlabel('Hour of Day')
plt.ylabel('Destination')
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x='destination', y='traffic_difference', data=df)
plt.xticks(rotation=90)
plt.title('Traffic Duration Outliers by Destination')
plt.xlabel('Destination')
plt.ylabel('Percent Time Difference')
plt.show()

df['average_speed_kph'].hist(bins=20)
plt.title('Distribution of Average Speed (kph)')
plt.xlabel('Average Speed (kph)')
plt.ylabel('Frequency')
plt.show()

df['traffic_adjusted'].value_counts().plot(kind='bar')
plt.title('Traffic Adjustment Categories')
plt.xlabel('Traffic Adjustment')
plt.ylabel('Frequency')
plt.show()