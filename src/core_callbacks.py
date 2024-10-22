import dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask_cors import CORS
from config.settings import CORS_IPS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_flask_app():
    """
    Create and configure the Flask app.
    """
    try:
        app = Flask(__name__)
        CORS(app, resources={r"/api/*":
                             {"origins": [CORS_IPS["appserver"], CORS_IPS["dashboard"]]}},
             methods=['GET', 'POST', 'OPTIONS'])
        logger.info("Flask app created and CORS configured.")
        return app
    except Exception as e:
        logger.error(f"Error creating Flask app: {e}")
        raise

def create_dash_app(flask_app):
    """
    Create and configure the Dash app.
    """
    try:
        external_stylesheets = [dbc.themes.BOOTSTRAP,
                                dbc.icons.BOOTSTRAP, '/static/styles.css']
        dash_app = dash.Dash(__name__, server=flask_app,
                             external_stylesheets=external_stylesheets, use_pages=True,
                             pages_folder='views')
        logger.info("Dash app created and configured.")
        return dash_app
    except Exception as e:
        logger.error(f"Error creating Dash app: {e}")
        raise

# Initialize Flask app
app = create_flask_app()

# Initialize Dash app
dash_app = create_dash_app(app)