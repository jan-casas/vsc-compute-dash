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
USER = 'admin'
PASSWORD = 'secret'

# API
IQAIR_WEATHER_API = '668e80e4-2704-4327-9ff7-6c671a673904'
AZURE_CHATBOT = 'j1tY_j1KQgc.VdI2DWSQsRtw_DcRP0of7bU9O0Rlos4jlLJKuqNWN1Q'
OPENAI_API_KEY = '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'
