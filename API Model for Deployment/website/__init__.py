from flask import Flask, jsonify
import folium
from openrouteservice import Client
from folium import plugins
import random

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = "1234samay5678ank"

    # from .views import views
    # from .auth import auth
    
    # app.register_blueprint(views, url_prefix = '/')
    # app.register_blueprint(auth, url_prefix = '/')

    return app