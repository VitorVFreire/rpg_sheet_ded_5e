import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from dotenv import load_dotenv
import os
import psycopg_pool

load_dotenv()

async def get_connection():
    pass

async def get_connection_without_async():
    conninfo = f'host={os.getenv("HOST")} dbname={os.getenv("DATABASE")} port={os.getenv("PORT")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    pool = psycopg_pool.AsyncConnectionPool(conninfo=conninfo, open=False)
    await pool.open()
    await pool.wait()
    return pool
