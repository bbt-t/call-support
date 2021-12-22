from loader import logger_guru
from config import adminsbot




async def on_startup_notify(dp):
    """
    Newsletter to admins when the bot is started
    """
    try:
        await dp.bot.send_message(adminsbot.get('creator'), 'Бот запущен')
    except Exception as err:
        logger_guru.warning(f'{repr(err)} : Сan not send a message to the administrator')


async def on_shutdown_notify(dp):
    """
    Newsletter to admins when the bot is stopped
    """
    try:
        await dp.bot.send_message(adminsbot.get('creator'), 'Бот остановлен!')
    except Exception as err:
        logger_guru.warning(f'{repr(err)} : Сan not send a message to the administrator')
