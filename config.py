from datetime import datetime
from os import getenv
import pytz

from dotenv import load_dotenv
load_dotenv()




adminsbot: dict = {
    'creator': getenv('creator'),
    'assistant': getenv('assistant')
}


BOT_TOKEN = getenv('BOT_TOKEN')

API_WEATHER = getenv('API_WEATHER')
API_WEATHER2 = getenv('API_WEATHER2')
CITY_WEATHER = getenv('CITY_WEATHER')

pkl_key = getenv('PKL_KEY')

FOLDER_ID = getenv('FOLDER_ID')
API_YA_STT = getenv('API_YA_STT')
API_YA_TTS = getenv('API_YA_TTS')

timezone = getenv('TIMEZONE')
time_zone = pytz.timezone(timezone)
time_now = time_zone.localize(datetime.now())

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
