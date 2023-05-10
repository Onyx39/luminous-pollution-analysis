"""
All the constants from the project
"""

import sys
from os import getenv

from sentinelhub.config import SHConfig
from dotenv import load_dotenv

load_dotenv('.env')

CLIENT_ID = getenv("CLIENT_ID")
INSTANCE_ID = getenv("INSTANCE_ID")
USER_SECRET = getenv("USER_SECRET")

START_DATE = "2023-01-01"  # Year-Month-Day
END_DATE = "2023-04-01"

DEPARTMENT = "23"

config = SHConfig()

if CLIENT_ID is None or INSTANCE_ID is None or USER_SECRET is None:
    print("env is not correctly set up.")
    sys.exit(-1)

config.instance_id = INSTANCE_ID
config.sh_client_id = CLIENT_ID
config.sh_client_secret = USER_SECRET
