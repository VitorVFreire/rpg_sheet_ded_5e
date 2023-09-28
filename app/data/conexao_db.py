import asyncio
import aiomysql
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

async def get_connection():
    loop = asyncio.get_event_loop()
    
    conn = await aiomysql.connect(host="localhost", user=os.getenv('USER_BASE'), password=os.getenv('PASSWORD_BASE'), db="RPG", loop=loop)
    
    return conn

def get_connection_without_async():
    conn = mysql.connector.connect(host="localhost", user=os.getenv('USER_BASE'), password=os.getenv('PASSWORD_BASE'), db="RPG")
    
    return conn