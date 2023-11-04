from flask import Flask, jsonify
import folium
from openrouteservice import Client
from folium import plugins
import random

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = "1234samay5678ank"
    
    return app