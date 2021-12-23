from aiogram.utils import executor

from loader import dp, scheduler, logger_guru
import utils.db.gino_shell_for_ORM_sqlalchemy as GINO


async def on_startup(dp):
    """
    Registration of handlers, middlewares, notifying admins about the start of the bot,
    an attempt to create a table User if it does not exist.
    :param dp: Dispatcher
    """
    import middlewares
    import handlers
    import filters
    #from utils.set_bot_commands import set_default_commands
    #await set_default_commands(dp)
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)

    await GINO.db_startup()
    #await GINO.db_shell.gino.drop_all()
    await GINO.db_shell.gino.create_all()


@logger_guru.catch()
async def on_shutdown(dp):
    """
    Notifying admins about the stop of the bot
    :param dp: Dispatcher
    """
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)

    await dp.storage.close()
    await dp.storage.wait_closed()

    await GINO.db_shutdown()
    raise SystemExit


if __name__ == '__main__':
    scheduler.start()
    try:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
    except BaseException as err:
        logger_guru.critical(f'{repr(err)} : STOP BOT')
