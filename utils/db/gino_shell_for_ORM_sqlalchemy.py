from sqlalchemy import inspect, Column, Table, DateTime

from config import POSTGRES_URL, time_now
from loader import db_shell, logger_guru




class BaseModel(db_shell.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: Table = inspect(self.__class__)
        primary_key_columns: list[Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())

        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db_shell.func.now())
    updated_at = Column(
        DateTime(True),
        default=time_now,
        onupdate=time_now,
        server_default=db_shell.func.now(),
    )


async def db_startup():
    logger_guru.info("Setup PostgreSQL Connection")
    await db_shell.set_bind(POSTGRES_URL)


async def db_shutdown():
    bind = db_shell.pop_bind()
    if bind:
        logger_guru.info("Close PostgreSQL Connection")
        await bind.close()
