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
COMPUTE_SCRIPTS = ['Dolcker/CeramicFacade']

# Database
DDBB_INFO = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}
PATH_DB_MODEL = os.getenv("PATH_DB_MODEL")
PATH_DATA_FOLDER = os.getenv("PATH_DATA_FOLDER")
