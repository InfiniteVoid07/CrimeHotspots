import folium
import random
import pandas as pd
from openrouteservice import Client

# Define the source and destination coordinates
# ls1 = float(input("Enter the latitude for the source: "))
# ls2 = float(input("Enter the longitude for the source: "))
# ld1 = float(input("Enter the latitude for the destination: "))
# ld2 = float(input("Enter the longitude for the destination:"))
ls1=28.73886
ls2=77.0500677
ld1=28.58281
ld2=77.08405 

# Create a map
m = folium.Map(location=[ls1, ls2], zoom_start=8)

locationsource = f"Latitude: {ls1}, Longitude: {ls2}"
locationdestin = f"Latitude: {ld1}, Longitude: {ld2}"
folium.Marker([ls1, ls2], icon=folium.Icon(color='green'), popup=locationsource).add_to(m)
folium.Marker([ld1, ld2], icon=folium.Icon(color='blue'), popup=locationdestin).add_to(m)

# Initialize empty lists to store the random data
crime_data = []

# Read the existing data from the CSV file
existing_data = pd.read_csv("crime_data.csv")

# Generate and display random data for latitude, longitude, type of crime, and time of crime
for _ in range(50):
    lat = random.uniform(ls1, ld1)
    long = random.uniform(ls2, ld2)

    # Generate random type of crime
    crime_types = ["Robbery", "Assault", "Burglary", "Theft", "Vandalism", "Fraud"]
    crime_type = random.choice(crime_types)

    # Generate a random time of crime (you can modify this as needed)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    time_of_crime = f"{hour:02d}:{minute:02d}"

    # Store the data in the list
    crime_data.append([lat, long, crime_type, time_of_crime])

    location = f"Latitude: {lat}, Longitude: {long}, Type of Crime: {crime_type}, Time of Crime: {time_of_crime}"

    # Add markers to the map
    folium.Marker([lat, long], icon=folium.Icon(color='gray'), popup=location).add_to(m)

# Calculate the mean (average) latitude and longitude of the random data
mean_latitude = sum(entry[0] for entry in crime_data) / len(crime_data)
mean_longitude = sum(entry[1] for entry in crime_data) / len(crime_data)

current_mean_location = f"Current Mean Location: Latitude {mean_latitude}, Longitude {mean_longitude}"

# Add a marker for the current mean location
folium.Marker([mean_latitude, mean_longitude], icon=folium.Icon(color='orange'), popup=current_mean_location).add_to(m)

# Draw an orange circle around the current mean location to indicate a danger zone
folium.Circle(location=[mean_latitude, mean_longitude], radius=len(crime_data) * (abs(ls1 - ld1)) / (abs(ls2 - ld2)), color='orange', fill=True, fill_color='orange').add_to(m)

# Calculate the overall mean by considering both the existing and random data
existing_latitudes = existing_data["Latitude"]
existing_longitudes = existing_data["Longitude"]

# Calculate the mean (average) of the existing latitude and longitude
existing_mean_latitude = existing_latitudes.mean()
existing_mean_longitude = existing_longitudes.mean()

overall_mean_latitude = (existing_mean_latitude + mean_latitude) / 2
overall_mean_longitude = (existing_mean_longitude + mean_longitude) / 2
overall_mean_location = f"Overall Mean Location: Latitude {overall_mean_latitude}, Longitude {overall_mean_longitude}"

# Add a marker for the overall mean location
folium.Marker([overall_mean_latitude, overall_mean_longitude], icon=folium.Icon(color='red'), popup=overall_mean_location).add_to(m)

# Draw a red circle around the overall mean location to indicate a danger zone (1000m radius)
folium.Circle(location=[overall_mean_latitude, overall_mean_longitude], radius=len(existing_data) * (abs(ls1 - ld1)) / (abs(ls2 - ld2)), color='red', fill=True, fill_color='red').add_to(m)

# Save the updated data back to the CSV file
updated_data = pd.concat([existing_data, pd.DataFrame(crime_data, columns=["Latitude", "Longitude", "Type of Crime", "Time of Crime"])], ignore_index=True)
updated_data.to_csv("crime_data.csv", index=False)

# Create a client for the OpenRouteService API (you need to sign up for an API key)
client = Client(key='5b3ce3597851110001cf62487728600986d14f3a8c4bce2711134303')

# Get the route between the source and destination coordinates
route = client.directions(coordinates=[[ls2, ls1], [ld2, ld1]], profile='driving-car', format='geojson')

# Create a GeoJSON layer for the route
route_layer = folium.GeoJson(route, name='Route')

# Add the route layer to the map
route_layer.add_to(m)

# Check if the route passes through the red circle area
route_coordinates = route["features"][0]["geometry"]["coordinates"]
for coord in route_coordinates:
    route_lat, route_lon = coord
    # Calculate the distance from the route point to the overall mean location
    distance = (abs(overall_mean_latitude - route_lat) * 111.32) + (abs(overall_mean_longitude - route_lon) * 111.32)
    
    # Check if the distance is less than the radius of the red circle (in meters)
    if distance < (len(existing_data) * (abs(ls1 - ld1)) / (abs(ls2 - ld2))):
        alert_message = "Alert: Route passes through a danger zone!"
        folium.Marker([route_lat, route_lon], icon=folium.Icon(color='red'), popup=alert_message).add_to(m)
        print(alert_message)

# Add Layer Control to toggle layers on/off
folium.LayerControl().add_to(m)
m.save("route_map.html")

