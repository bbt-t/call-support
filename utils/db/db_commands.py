from asyncpg import UniqueViolationError

from loader import logger_guru
from utils.db.db_table.users import Users




async def add_user(telegram_id: int, full_name: str, user_name: str = None, email: str = None):
    try:
        await Users(telegram_id=telegram_id, full_name=full_name, user_name=user_name, email=email).create()
    except UniqueViolationError:
        logger_guru.info('Trying to add an existing user')


async def select_users(telegram_id: int):
    selected_user = await Users.query.where(Users.telegram_id == telegram_id).gino.first()
    return selected_user


async def select_all_users():
    return await Users.query.gino.all()


async def update_email(telegram_id, email):
    user_obj = await Users.get(telegram_id)
    await user_obj.update(email=email).apply()
