import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from dotenv import load_dotenv
import os
import psycopg_pool

load_dotenv()

class Db:
    def __init__(self):
        self.host = os.getenv('HOST')
        self.database = os.getenv('DATABASE')
        self.port = os.getenv('PORT')
        self.user_db = os.getenv('USER')
        self.password_db = os.getenv('PASSWORD')
        self.pool = None
            
    async def connection_db(self):
        conninfo = f'host={self.host} dbname={self.database} port={self.port} user={self.user_db} password={self.password_db}'
        self.pool = psycopg_pool.AsyncConnectionPool(conninfo=conninfo, open=False)
        await self.pool.open()
        await self.pool.wait()
        
    async def select(self, query, parameters = (), all=True):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    result = await cursor.fetchall() if all is True else await cursor.fetchone()
                    await cursor.close()
                    return result
        except Exception as e:
            print(e)
            return None
        finally:
            await self.pool.close()
    
    async def insert(self, query, parameters):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    result = await cursor.fetchone()
                    await cursor.close()
                    return result
        except Exception as e:
            print(e)
            return None
        finally:
            await self.pool.close()
            
    async def update(self, query, parameters):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    await cursor.close()
                    return True
        except Exception as e:
            print(e)
            return False
        finally:
            await self.pool.close()
            
    async def delete(self, query, parameters):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    await cursor.close()
                    return True
        except Exception as e:
            print(e)
            return False
        finally:
            await self.pool.close()
    
    async def exists(self, query, parameters):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    result = await cursor.fetchone()
                    if result[0] == 1:
                        return True
        except Exception as e:
            print(e)
            return False
        finally:
            await self.pool.close()
        