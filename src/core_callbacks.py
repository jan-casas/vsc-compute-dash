import dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask_cors import CORS

# Load environment variables
external_stylesheets = [dbc.themes.BOOTSTRAP,
                        dbc.icons.BOOTSTRAP, '/static/styles.css']

# Define Flask app
app = Flask(__name__)

# Enable CORS for the specified origins and HTTP methods
CORS(app, resources={r"/api/*": {"origins": [
    'http://localhost:3000',  # JS app (Rhino.compute)
    'http://127.0.0.1:5000'  # Python app (Dashboard)
]}}, methods=['GET', 'POST', 'OPTIONS'])

# Define Dash app
dash_app = dash.Dash(__name__, server=app,
                     external_stylesheets=external_stylesheets, use_pages=True,
                     pages_folder='views')
