from datetime import datetime
from os import getenv
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
load_dotenv()


adminsbot: dict = {
    'creator': getenv('creator'),
    'assistant': getenv('assistant')
}


BOT_TOKEN = getenv('BOT_TOKEN')

timezone = getenv('TIMEZONE')
time_now = datetime.now(ZoneInfo(timezone))

HOST = getenv('HOST')

PORT_REDIS = getenv('PORT_REDIS')
PASS_REDIS = getenv('PASS_REDIS')

redis = {
    'host': HOST,
    'port': PORT_REDIS,
    'password': PASS_REDIS,
    'prefix': 'fsm_key'
}

DB_NAME = getenv('DB_NAME')
