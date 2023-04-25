from os import getenv
from dotenv import load_dotenv
from sentinelhub import (
    SHConfig
)

load_dotenv('.env')

CLIENT_ID = getenv("CLIENT_ID")
INSTANCE_ID = getenv("INSTANCE_ID")
USER_SECRET = getenv("USER_SECRET")

START_DATE = "2023-01-01" # Year-Month-Day
END_DATE = "2023-04-01"

POSSIBLE_RESOLUTIONS = [10, 20, 60]

config = SHConfig()

config.instance_id = INSTANCE_ID
config.sh_client_id = CLIENT_ID
config.sh_client_secret = USER_SECRET
