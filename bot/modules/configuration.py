import os

from dotenv import load_dotenv

logging = {}
database = {}

load_dotenv()
token = os.getenv("STADIA_ITALIA_DISCORD_TOKEN")
logging_level = os.getenv("STADIA_ITALIA_LOGGING_LEVEL")
user = os.getenv("STADIA_ITALIA_DATABASE_USER")
password = os.getenv("STADIA_ITALIA_DATABASE_PASSWORD")
db_name = os.getenv("STADIA_ITALIA_DATABASE")
host = os.getenv("STADIA_ITALIA_DATABASE_HOST")
repository = os.getenv("STADIA_ITALIA_CONFIGURATION_COLLECTION")
