from dotenv import load_dotenv
import datetime as dt
from os import getenv
load_dotenv('.env')

CLIENT_ID = getenv("CLIENT_ID")
INSTANCE_ID = getenv("INSTANCE_ID")
USER_SECRET = getenv("USER_SECRET")

EVALSCRIPT_PATH = "custom.js"

IMAGE_RESOLUTION = 10

START_DATE = "2023-01-01" # Year-Month-Day
END_DATE = "2023-04-01"

MAX_CLOUD_COVERAGE = 0.3