from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from gino import Gino
from loguru import logger as logger_guru

from config import BOT_TOKEN, redis




storage = RedisStorage2(**redis)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

db_shell = Gino()

scheduler = AsyncIOScheduler()
scheduler.configure(
    jobstores={'default': SQLAlchemyJobStore(url='sqlite:///data/jobs.sqlite')},
    logger=logger_guru)

logger_guru.add(
    'logging-bot-support.log',
    format='{time} {level} {message}',
    level='WARNING',
    rotation='00:00',
    compression='gz',
    )
