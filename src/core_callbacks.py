import logging
import sys

import dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask_cors import CORS

# Load environment variables
external_stylesheets = [dbc.themes.BOOTSTRAP,
                        dbc.icons.BOOTSTRAP, '/static/styles.css']

# Define Flask app
app = Flask(__name__)
# Enable CORS for all endpoints of the app (the js app return errors if not)
CORS(app)
CORS(app, origins=[
    'http://localhost:3000',  # JS app Rhino.compute    TODO Change this to the production URL
    'http://localhost:8000'  # Python app Dashboard
])

# Define Dash app
dash_app = dash.Dash(__name__, server=app,
                     external_stylesheets=external_stylesheets, use_pages=True,
                     pages_folder='views')
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)],
                    format='%(asctime)s - %(levelname)s - %(message)s')
