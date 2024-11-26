# AIPI510-Final-Dataset-Project

# Code Repository
https://github.com/JesseFWarren/AIPI510-Final-Dataset-Project

This repository contains all of my scripts used for collecting, processing, and analyzing traffic data across the largest US cities. The files include:  

data_collection.py: Automates data retrieval using the Google Distance Matrix API.  
feature_engineering.py: Adds new features and cleans the dataset.  
data_exploratory_analysis: Contains code for exploratory data analysis and visualizations.  
traffic_data_with_features.csv: The final dataset with additional engineered features.  

# Executive Summary

This dataset provides a comprehensive analysis of travel times and traffic delays from Durham, North Carolina to the 50 largest cities in the United States, addressing the growing need to understand how traffic impacts travel efficiency. By collecting real-time data on distances, durations, and delays, the dataset is designed to help commuters, city planners, and businesses make better decisions related to transportation and logistics.  

What makes this dataset unique is its level of detail and focus. While existing traffic datasets often cover broader trends or specific regions, this dataset focuses on hourly, real-time data that captures the nuances of traffic patterns in urban areas. It also includes calculated metrics like average speed and traffic delay factors, offering insights that go beyond simple travel times. Futhermore, it is relavent to us here at Duke as all the data is travel times from Durham, North Carolina. Compared to other datasets in this domain, such as Google Traffic Reports or static Department of Transportation datasets, this one stands out because of its dynamic approach to understanding traffic conditions as it relates to Duke Students.  

The data was ethically sourced using the Google Distance Matrix API to ensure accuracy and reliability. However, there are potential biases to consider:  
City focus: The dataset is limited to travel to large cities and doesn’t include travel to rural or suburban areas.
Time-specific: Data collection was done during a specific time frame, which might not reflect seasonal or long-term changes.
API dependency: Traffic estimates are based on Google’s algorithms, which may carry inherent biases.  

By recognizing these limitations, the dataset remains transparent while providing valuable insights. This resource can be applied in many ways:  
City planning: To identify traffic hotspots and improve infrastructure.  
Business logistics: To optimize delivery routes and schedules.  
Commuter tools: To create more accurate navigation systems.  
Research: To study the effects of urban traffic on mobility and productivity.  

# Description of Data

Source: Google Distance Matrix API.
Data Points:  
Origin city: Durham, North Carolina  
Destination cities: 50 large US Cities.  
Distance: Distance between origin and destination in km.  
Duration: The duration to drive between the cities without accounting for real time traffic conditions.  
Duration in traffic: The duration to drive between the cities accounting for real time traffic conditions.  
Timestamp: The time at which the data was collected.  

Derived features:   
distance km: distance without km units.  
duration minutes: duration in minutes without unit label.  
duration in traffic minutes: duration in traffic in minutes without unit label.  
Traffic difference: Percent difference in travel time with and without traffic.  
Average speed: Travel speed considering traffic delays.  
Traffic delay factor: Average delay per km due to traffic.  
Traffic adjusted: Faster, Slower, or Same, based on traffic difference.  

Size: Includes hourly data collection for 50 destinations over 24 hours.  

# Power Analysis Results

After some research regarding the effect size used for similar dataset creation. I 
have chosen to use a effect size of 0.3. Additionally, I will use an alpha of 0.05 and a power of 0.8.
Thus, the sample size needed is 175. However, I have gathered more data than this.  
Null Hypothesis (H₀): Traffic conditions do not significantly affect the overall travel duration between destinations.  
Alternative Hypothesis (H₁): Traffic conditions significantly affect the overall travel duration between destinations.

# Exploratory Data Analysis
Key Visualizations used in analysis:  
1. Distance vs. Duration Scatterplot:  
Shows the relationship between trip distance and travel time.  
Reveals outliers where short distances have disproportionally high travel durations.  

2. Average Travel Time Percent Difference by Hour:  
Displays the percentage impact of traffic by hour.  
Highlights peak and low traffic times.  
Traffic delay peaks sharply during morning rush hours (7–9 AM) and evening rush hours (4–7 PM), which is consistent with expected commuter traffic.  
Late-night travel (12–5 AM) experiences minimal delays, with some trips even completing faster than expected due to low traffic levels.  

3. Average Travel Time Percent Difference by Destination:  
Compares traffic impact across cities.  
Cities like Boston, New York, and Baltimore experience the highest delays.  
Trips that take you through large cities often have higher delays.  
Destinations such as Raleigh and Charlotte which are closer have much lower delays as expected.  

4. Traffic Delay Heatmap:  
Heatmap of traffic delay across hours and destinations.  
Shows trends in specific cities at specific times.  
Cities like New York, Los Angeles, and Boston show consistent delays throughout the day, particularly during peak hours.  
Mid-sized cities like Omaha and Tulsa exhibit more sporadic traffic delays due to less intense commuter activity.  

4. Traffic Adjustment Categories:  
Bar chart categorizing routes accounting for traffic as "Faster," "Same," or "Slower" than the trip not accounting for traffic.  
A majority of trips are "Faster" and indicate durations shorter than estimated, possibly due to real-time adjustments by the Google API based on light traffic conditions.  
About 25% of trips fall under "Same", where actual traffic did not significantly impact travel time.  
A small percentage of trips (categorized as "Slower") reveal significant delays, often concentrated in high-traffic cities and during peak hours.
Therefore, traffic delays do not have as high of an impact on travel time as one may think.  

5. Distribution of Average Speed:
Histogram displaying the frequency of average speed values, showing most trips occur between 100–110 km/h.  
The histogram reveals a tight clustering of speeds between 100–110 km/h. Since most trips take place on highways or major roads, this makes sense.  

6. Boxplot of Traffic Duration Outliers:  
The whiskers and outliers on the boxplot emphasize how certain cities deviate from their typical traffic patterns.  
Cities like New York and Boston show significant variability in traffic delays. With several extreme outliers indicating unpredictable traffic conditions.  
However, cities like Raleigh and Charlotte show minimal variation, suggesting consistent travel conditions.  

7. Additional Insights and Actional Recommendations from Analysis:  
Rush hours consistently show the highest delays.  
Late-night hours (12–5 AM) consistently show the shortest travel durations.  
Avoid travel during peak commuter hours in cities like New York and Boston.  
Plan trips at less congested travel times like early in the morning.  
This dataset can help identify areas where traffic congestion is a persistent issue.  
Further data collection could help reveal further trends over a larger period of time.  

# License

This dataset is distributed under the CC0 1.0 Universal (CC0 1.0 Public Domain Dedication). Meaning anyone is free to copy, modify, and distribute this dataset for both personal and commercial purposes.

# Ethics Statement

The dataset was ethically sourced from public APIs (Google Distance Matrix API) using an API key and following all usage policies. Data collection was automated hourly to ensure unbiased and consistent sampling. Although there is a potential geographic bias as I focused on US cities as well as a small sample size for dates, I address this limitation in our analysis.
