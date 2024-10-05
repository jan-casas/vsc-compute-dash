import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Speckle
SPECKLE_HOST = os.getenv("SPECKLE_HOST", "https://app.speckle.systems")
SPECKLE_PROJECT = os.getenv("SPECKLE_PROJECT")
SPECKLE_MODEL_ID = os.getenv("SPECKLE_MODEL_ID")
SPECKLE_INITIAL_COMMIT_ID = os.getenv("SPECKLE_INITIAL_COMMIT_ID")
MODEL_TESTING = os.getenv("MODEL_TESTING")
UNWANTED_FIELDS = ['id', 'totalChildrenCount', 'applicationId']

# Compute
CORS_IPS = {
    "appserver": os.getenv("CORS_APPSERVER"),  # JS app (Rhino.compute)
    "dashboard": os.getenv("CORS_DASHBOARD"),  # Python app (Dashboard)
}
COMPUTE_PATHS = {
    "appserver": os.getenv("APPSERVER_PATH"),
    "node": os.getenv("NODE_PATH"),
    "npm": os.getenv("NPM_PATH"),
    "compute": os.getenv("COMPUTE_GEOMETRY_PATH"),
}
COMPUTE_SCRIPTS = ['Corbalán/uglass_facade_tint', 'Garnica/wood_panel_wall',
                   'Garnica/wood_panel_floor',
                   'Garnica/wood_panel_ceiling']
