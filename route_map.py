import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Load CSV file
file_path = "./chitomi.csv"  # Update with actual file path
df = pd.read_csv(file_path, parse_dates=['Time_Stamp'])

# Rename columns for better readability
df = df.rename(columns={'Time_Stamp': 'timestamp', 'Lat': 'latitude', 'Lng': 'longitude', 'Velocity': 'speed'})

# Drop rows with missing latitude, longitude, or timestamp
df = df.dropna(subset=['latitude', 'longitude', 'timestamp'])

# Interpolate missing speed values if necessary
df['speed'] = df['speed'].interpolate()

# Initialize Folium map centered at the first valid point
map_center = [df.iloc[0]['latitude'], df.iloc[0]['longitude']]
route_map = folium.Map(location=map_center, zoom_start=15)

# Draw the route as a polyline to connect points
coordinates = list(zip(df['latitude'], df['longitude']))
folium.PolyLine(coordinates, color="blue", weight=4, opacity=0.7).add_to(route_map)

# Prepare features for animation (tracking movement over time)
features = []
for _, row in df.iterrows():
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["longitude"], row["latitude"]]
        },
        "properties": {
            "time": row["timestamp"].isoformat(),  # Ensure correct time format
            "popup": f"Speed: {row['speed']:.2f} km/h",
            "icon": "circle",
            "iconstyle": {
                "fillColor": "red",
                "fillOpacity": 0.6,
                "stroke": "true",
                "radius": 5
            }
        }
    })

# Add the animated route to the map
TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="PT0.1S",  # Set 100ms intervals
    add_last_point=True,
    auto_play=True,
    loop=True,
    max_speed=1,
    transition_time=500  # Adjust transition speed
).add_to(route_map)

# Save and display map
route_map.save("animated_route_map.html")
route_map
