import folium
import random
import pandas as pd
from openrouteservice import Client



# Define the source and destination coordinates

ls1 = float(input("Enter the latitude for the source: "))
ls2 = float(input("Enter the longitude for the source: "))
ld1 = float(input("Enter the latitude for the destination: "))
ld2 = float(input("Enter the longitude for the destination:"))

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
    print(location)

# Calculate the mean (average) latitude and longitude of the random data
mean_latitude = sum(entry[0] for entry in crime_data) / len(crime_data)
mean_longitude = sum(entry[1] for entry in crime_data) / len(crime_data)

# Calculate the overall mean by considering both the existing and random data

current_mean_location=f"Current Mean Location: Latitude {mean_latitude}, Longitude{mean_longitude}"

#add a marker for current mean location
folium.Marker([mean_latitude, mean_longitude], icon=folium.Icon(color='orange'), popup=current_mean_location).add_to(m)
#folium.Circle(location=[overall_mean_latitude, overall_mean_longitude], radius=1000, color='red', fill=True, fill_color='red').add_to(m)

#draw a orange circle arpound the current mean location to indicate a danger zone
folium.Circle(location=[mean_latitude, mean_longitude], radius=len(crime_data)*(abs(ls1-ld1))/(abs(ls2-ld2)), color='orange', fill=True, fill_color='orange').add_to(m)


print(current_mean_location)



# Create a client for the OpenRouteService API (you need to sign up for an API key)
client = Client(key='5b3ce3597851110001cf62487728600986d14f3a8c4bce2711134303')

    # Get the route between the source and destination coordinates
route = client.directions(coordinates=[[ls2, ls1], [ld2, ld1]], profile='driving-car', format='geojson')

    # Create a GeoJSON layer for the route
route_layer = folium.GeoJson(route, name='Route')

    # Add the route layer to the map
route_layer.add_to(m)

# Create a DataFrame from the new crime_data list
new_data = pd.DataFrame(crime_data, columns=["Latitude", "Longitude", "Type of Crime", "Time of Crime"])



# Concatenate the existing data with the new data
updated_data = pd.concat([existing_data, new_data], ignore_index=True)


# Extract latitude and longitude from the existing data
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
folium.Circle(location=[overall_mean_latitude, overall_mean_longitude], radius=len(existing_data)*(abs(ls1-ld1))/(abs(ls2-ld2)), color='red', fill=True, fill_color='red').add_to(m)
print(overall_mean_location)



# Save the updated data back to the CSV file
updated_data.to_csv("crime_data.csv", index=False)
# Add Layer Control to toggle layers on/off
folium.LayerControl().add_to(m)

# Save the map as an HTML file
# m.save("random_locations_with_mean_and_danger_zone.html")


from shapely.geometry import Point
from folium import Marker, GeoJson, Map

# Define the center and radius of the circular red zone
red_zone_center = (overall_mean_latitude, overall_mean_longitude)  # Replace with the center coordinates
red_zone_radius =  len(existing_data)*(abs(ls1-ld1))/(abs(ls2-ld2))

# Your route data (modify as needed)
route_coordinates = [(ls1, ls2), (ld1, ld2)]  # Replace with your route's coordinates
route_line = [(lat, lng) for lat, lng in route_coordinates]  # Shapely works with (lon, lat) format

# Check if the route intersects with the circular red zone
route_intersects_red_zone = any(Point(coord).distance(Point(red_zone_center)) <= red_zone_radius for coord in route_line)

# Add the route as a GeoJSON layer (modify as needed)
route_layer = folium.GeoJson(route, name='Route')
route_layer.add_to(m)

# Check if the route intersects with the circular red zone
if route_intersects_red_zone:
    # overall_mean_location = f"Overall Mean Location: Latitude {overall_mean_latitude}, Longitude {overall_mean_longitude}"
    alert_message = f"Alert: The route passes through the red zone!"
    # alert_marker = Marker(location=(overall_mean_latitude,longitude), popup=alert_message, icon=None)
    folium.Marker([overall_mean_latitude, overall_mean_longitude], icon=folium.Icon(color='red'), popup=alert_message).add_to(m)

# Save the map as an HTML file
m.save("route_map.html")

# Save the map as an HTML file
m.save("random_locations_with_mean_and_danger_zone.html")




