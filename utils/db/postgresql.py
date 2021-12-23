from typing import Optional
from asyncpg.pool import Pool
from asyncpg import create_pool, Connection

from config import DB_PASS, DB_HOST, DB_NAME, DB_USER




class DataBase:
    def __init__(self):
        self.pool: Pool = Optional[Pool]

    async def create_pool(self):
        self.pool = await create_pool(password=DB_PASS, host=DB_HOST, database=DB_NAME, user=DB_USER)

    async def execute(self, command, *args,
                      fetch: bool = False, fetchval: bool = False, fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connect:
            connect: Connection
            async with connect.transaction():
                if fetch:
                    result = await connect.fetch(command, *args)
                elif fetchval:
                    result = await connect.fetchval(command, *args)
                elif fetchrow:
                    result = await connect.fetchrow(command, *args)
                elif execute:
                    result = await connect.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users
        (
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(128) NOT NULL,
            user_name VARCHAR(128) NULL,
            email VARCHAR(256) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def select_all_users(self):
        sql = 'SELECT * FROM users'
        return self.execute(sql, fetch=True)
