import asyncio
import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

async def get_connection():
    loop = asyncio.get_event_loop()
    
    conn = await aiomysql.connect(host="localhost", user=os.getenv('USER_BASE'), password=os.getenv('PASSWORD_BASE'), db="RPG", loop=loop)
    
    return conn