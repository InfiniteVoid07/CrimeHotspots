from flask import Flask, render_template
import folium
from openrouteservice import Client
from folium import plugins
import random

app = Flask(__name__)

@app.route('/')
def index():
    ls1 = 28.58281
    ls2 = 77.05006
    ld1 = 28.73886
    ld2 = 77.08405

    m = folium.Map(location=[ls1, ls2], zoom_start=12.5)
    locationsource = f"Latitude: {ls1}, Longitude: {ls2}"
    locationdestin = f"Latitude: {ld1}, Longitude: {ld2}"
    folium.Marker([ls1, ls2], icon=folium.Icon(color='green'), popup=locationsource).add_to(m)
    folium.Marker([ld1, ld2], icon=folium.Icon(color='blue'), popup=locationdestin).add_to(m)

    client = Client(key='5b3ce3597851110001cf62487728600986d14f3a8c4bce2711134303')
    route = client.directions(coordinates=[[ls2, ls1], [ld2, ld1]], profile='driving-car', format='geojson')
    route_layer = folium.GeoJson(route, name='Route')
    route_layer.add_to(m)

    heatdata = []
    for _ in range(50):
        lat = random.uniform(ls1, ld1)
        long = random.uniform(ls2, ld2)
        heatdata.append([lat, long])
    plugins.HeatMap(heatdata).add_to(m)

    m.save("./website/templates/source_to_destination_route_with_heatmap.html")  # Save the map inside the Flask templates folder

    return render_template('source_to_destination_route_with_heatmap.html')

if __name__ == '__main__':
    app.run(debug=True)
