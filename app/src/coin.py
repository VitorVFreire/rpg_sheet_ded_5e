import asyncio
from src import Db

class Coin:
    def __init__(self,coin_id=None, coin_name=None):
        self._coin_id = coin_id or[]
        self._coin_name = coin_name or []
        
    @property
    def coin_name(self):
        return self._coin_name
    
    @property
    def coin_id(self):
        return self._coin_id
    
    @property
    async def coins(self):
        if (type(self._coin_id) is list and len(self._coin_id)<=0) or (self._coin_id is None):
            await self.load_coins()
        coins = []
        for coin_id, coin_name in zip(self._coin_id, self._coin_name):
            coins.append({'coin_id': coin_id, 'coin_name': coin_name})
        return coins
    
    async def load_coins(self):
        try:
            query = "SELECT coin_id, coin_name FROM coin;"
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                for row in result:
                    self._coin_id.append(row[0])
                    self._coin_name.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_coin(self):
        try:
            query = "SELECT coin_name FROM coin WHERE coin_id=%s;"
            parameters = (self._coin_id,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._coin_name=result[0]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_coin_with_name(self):
        try:
            query = "SELECT coin_id FROM coin WHERE coin_name=%s;"
            parameters = (self._coin_name,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._coin_id=result[0]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_coin(self):
        try:
            query = "INSERT INTO coin (coin_name) VALUES (%s) RETURNING coin_id;"
            parameters = (str(self._coin_name),)
            db = Db()
            await db.connection_db()
            self._coin_id = await db.insert(query=query, parameters=parameters)
            return True
        except Exception as e:
            print(e)
            return False
        
    async def delete_coin(self):
        try:
            query = "DELETE from coin WHERE coin_id=%s;"
            parameters = (self._coin_id,)
            db = Db()
            await db.connection_db()
            return await db.delete(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False
        
    async def update_coin(self, value):
        try:
            query = "UPDATE coin SET coin_name=%s WHERE coin_id=%s;"
            parameters = (value, self._coin_id)
            db = Db()
            await db.connection_db()
            return await db.update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False  