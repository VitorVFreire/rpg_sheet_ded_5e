from data import get_connection
import asyncio
from src import Db

class Race:
    def __init__(self,race_id=None,race_name=None):
        self._race_id = race_id or[]
        self._race_name = race_name or []
        
    @property
    def race_name(self):
        return self._race_name
    
    @property
    def race_id(self):
        return self._race_id
    
    @property
    async def races(self):
        if (type(self._race_id) is list and len(self._race_id)<=0) or (self._race_id is None):
            await self.load_races()
        racas = []
        for race_id, race_name in zip(self._race_id, self._race_name):
            racas.append({'race_id': race_id, 'race_name': race_name})
        return racas
    
    async def load_races(self):
        try:
            query = "SELECT race_id, race_name FROM race;"
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                for row in result:
                    self._race_id.append(row[0])
                    self._race_name.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_race(self):
        try:
            query = "SELECT race_name FROM raca WHERE race_id=%s;"
            parameters = (self._race_id,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._race_name=result[0]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_race(self):
        try:
            query = "INSERT INTO raca (race_name) VALUES (%s);"
            parameters = (str(self._race_name),)
            db = Db()
            await db.connection_db()
            self._race_id = await db.insert(query=query, parameters=parameters)
            return True
        except Exception as e:
            print(e)
            return False
        
    async def delete_race(self):
        try:
            query = "DELETE from raca WHERE race_id=%s;"
            parameters = (self._race_id,)
            db = Db()
            await db.connection_db()
            return await db.delete(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False
        
    async def update_race(self, value):
        try:
            query = "UPDATE raca SET race_name=%s WHERE race_id=%s"
            parameters = (value, self._race_id)
            db = Db()
            await db.connection_db()
            return await db.update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False        