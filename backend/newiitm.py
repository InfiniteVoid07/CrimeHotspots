import folium
import random
from openrouteservice import Client
from shapely.geometry import Polygon, Point

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
points_within_route = []

for _ in range(100):
    lat = random.uniform(ls1, ld1)
    long = random.uniform(ls2, ld2)
    point = Point(long, lat)
    
    # Check if the point is within the geofence
    if route_polygon.contains(point):
        points_within_route.append(point)

# Add markers for points within the route
for point in points_within_route:
    lat, lon = point.y, point.x
    folium.CircleMarker(
        location=[lat, lon],
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
    ).add_to(m)

# Create a GeoJSON layer for the geofence
folium.GeoJson(route_polygon, name='Geofence', style_function=lambda x: {'color': 'blue'}).add_to(m)

# Save the map to an HTML file
m.save("source_to_destination_route_with_geofence_legend.html")

