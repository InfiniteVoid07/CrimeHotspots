import folium
import random
from openrouteservice import Client
from shapely.geometry import Polygon, Point
import pandas as pd
from datetime import datetime, timedelta

# Define the source and destination coordinates
ls1 = 28.58281
ls2 = 77.05006
ld1 = 28.73886
ld2 = 77.08405


# Create a map
m = folium.Map(location=[ls1, ls2], zoom_start=12.5)

locationsource = f"Latitude: {ls1}, Longitude: {ls2}"
locationdestin = f"Latitude: {ld1}, Longitude: {ld2}"
folium.Marker([ls1, ls2], icon=folium.Icon(color='green'), popup=locationsource).add_to(m)
folium.Marker([ld1, ld2], icon=folium.Icon(color='blue'), popup=locationdestin).add_to(m)

# Create a legend
legend_html = """
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 150px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color: white;
     opacity: 0.8;
     ">
     <p>Legend</p>
     <p><i class="fa fa-map-marker fa-2x" style="color:green"></i> Source</p>
     <p><i class="fa fa-map-marker fa-2x" style="color:blue"></i> Destination</p>
     <p><i class="fa fa-circle fa-2x" style="color:red"></i> Points within Route</p>
</div>
"""

legend = folium.Element(legend_html)
legend.add_to(m)

client = Client(key='5b3ce3597851110001cf62487728600986d14f3a8c4bce2711134303')

# Get the route between the source and destination coordinates
route = client.directions(coordinates=[[ls2, ls1], [ld2, ld1]], profile='driving-car', format='geojson')

route_layer = folium.GeoJson(route, name='Route')
route_layer.add_to(m)

# Extract route coordinates
route_coordinates = route['features'][0]['geometry']['coordinates']

# Create a Polygon from the route coordinates to define the geofence
route_polygon = Polygon(route_coordinates)

# Generate random data for points
crime_data = []

for _ in range(40):
    lat = random.uniform(ls1, ld1)
    lon = random.uniform(ls2, ld2)
    crime_name = random.choice(["Murder", "Rape", "Robbery", "Assault", "Traffic Violence", "Disorderly Conduct"])
    
    # Generate a random date within the last 4 years
    today = datetime.now()
    start_date = today - timedelta(days=4*365)
    random_date = start_date + timedelta(days=random.randint(0, 4*365))
    date_str = random_date.strftime("%Y-%m-%d")
    
    # Generate a random time
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    time_str = f"{hour:02d}:{minute:02d}"
    
    crime_data.append([lat, lon, crime_name, date_str, time_str])



existing_data = pd.read_csv("crime_data_generated.csv")
updated_data = pd.concat([existing_data, pd.DataFrame(crime_data, columns=["Latitude", "Longitude", "CrimeName", "Date", "Time"])], ignore_index=True)
updated_data.to_csv("crime_data_generated.csv", index=False)
# crime_df.to_csv("crime_data_generated.csv", index=False)
dict={"Murder":'red',"Rape":'red',"Robbery":'yellow',"Assault":'yellow',"Traffic Violence":'blue',"Disorderly Conduct":'blue'}
dict2={"Murder":150,"Rape":360,"Robbery":30,"Assault":14,"Traffic Violence":7,"Disorderly Conduct":14}
# Save the generated crime data to a CSV file
crime_df = pd.DataFrame(updated_data, columns=["Latitude", "Longitude", "CrimeName", "Date", "Time"])

# Iterate over the crime data and add markers for each crime location
for index, row in crime_df.iterrows():
    lat, lon, crime_name, date, time = row['Latitude'], row['Longitude'], row['CrimeName'], row['Date'], row['Time']
    point = Point(lon, lat)
    # Check if the point is within the geofence
    # Get the current date
    current_date = datetime.now()
    # Calculate the difference between the current date and the random date
    date_format = "%Y-%m-%d"
    # Use datetime.strptime to convert the string to a date
    date = datetime.strptime(date, date_format)
    date_difference = current_date - date
    dayyy=date_difference.days
    d=dict2[crime_name]
    if route_polygon.contains(point):
        if (d<=dayyy):
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                color=dict.get(crime_name),
                fill=True,
                fill_color=dict.get(crime_name),
                fill_opacity=1.0,
                popup=f"Crime: {crime_name}<br>Date: {date}<br>Time: {time}"
            ).add_to(m)
        else:
            folium.CircleMarker(
                location=[lat, lon],
                radius=3,
                color="grey",
                fill=True,
                fill_color="grey",
                fill_opacity=1.0,
                popup=f"Crime: {crime_name}<br>Date: {date}<br>Time: {time}"
            ).add_to(m)

# Create a GeoJSON layer for the geofence
folium.GeoJson(route_polygon, name='Geofence', style_function=lambda x: {'color': 'blue'}).add_to(m)

# Save the map to an HTML file
m.save("source_to_destination_route_with_geofence_legend_crime_data_generated.html")


