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
SPECKLE_PROJECT = os.getenv("SPECKLE_PROJECT", "013613abb4")
SPECKLE_MODEL_ID = os.getenv("SPECKLE_STREAM_ID", "c6734eae44")
SPECKLE_INITIAL_COMMIT_ID = os.getenv("SPECKLE_INITIAL_COMMIT_ID", "@a33f2acd4c")
MODEL_TESTING = os.getenv("MODEL_TESTING",
                          "https://app.speckle.systems/projects/013613abb4/models/c6734eae44"
                          "@a33f2acd4c")
UNWANTED_FIELDS = ['id', 'totalChildrenCount', 'applicationId']

# Compute
compute_scripts = ['Corbalán/uglass_facade_tint', 'Garnica/wood_panel_wall',
                   'Garnica/wood_panel_floor',
                   'Garnica/wood_panel_ceiling']
