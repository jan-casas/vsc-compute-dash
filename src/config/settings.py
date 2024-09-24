import logging
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_DATABASE")
PORT = os.getenv("DB_PORT")

# Azure chatbot
AZURE_CHATBOT = os.getenv("AZURE_CHATBOT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Flask
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

# API
IQAIR_WEATHER_API = os.getenv("IQAIR_WEATHER_API")
AZURE_CHATBOT = os.getenv("AZURE_CHATBOT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Speckle
SPECKLE_HOST = os.getenv("SPECKLE_HOST", "https://app.speckle.systems")
SPECKLE_PROJECT = os.getenv("SPECKLE_PROJECT", "013613abb4")
SPECKLE_MODEL_ID = os.getenv("SPECKLE_STREAM_ID", "c6734eae44")
SPECKLE_INITIAL_COMMIT_ID = os.getenv("SPECKLE_INITIAL_COMMIT_ID", "@a33f2acd4c")
MODEL_TESTING = os.getenv("MODEL_TESTING",
                          "https://app.speckle.systems/projects/013613abb4/models/c6734eae44"
                          "@a33f2acd4c")

# Logging
# logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
# Suppress all Speckle-related logs
for logger_name in logging.root.manager.loggerDict:
    if logger_name.startswith('specklepy'):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.CRITICAL)
        logger.propagate = False
