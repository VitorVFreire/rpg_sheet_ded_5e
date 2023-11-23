import asyncio
from src import Db

class SavingThrow:
    def __init__(self, saving_throw_id = None, saving_throw_name = None):
        self._saving_throw_id = saving_throw_id or []
        self._saving_throw_name = saving_throw_name or []
        
    @property
    def saving_throw_name(self):
        return self._saving_throw_name
    
    @property
    def saving_throw_id(self):
        return self._saving_throw_id
    
    @property
    async def saving_throws(self):
        if (type(self._saving_throw_id) is list and len(self._saving_throw_id)<=0) or (self._saving_throw_id is None):
            await self.load_saving_throws()
        saving_throws = []
        for saving_throw_id, saving_throw_name in zip(self._saving_throw_id, self._saving_throw_name):
            saving_throws.append({'saving_throw_id': saving_throw_id, 'saving_throw_name': saving_throw_name})
        return saving_throws
    
    async def load_saving_throws(self):
        try:
            query = "SELECT saving_throw_id, saving_throw_name FROM saving_throw;"
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                for row in result:
                    self._saving_throw_id.append(row[0])
                    self._saving_throw_name.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_saving_throw(self):
        try:
            query = "SELECT saving_throw_name FROM saving_throw WHERE saving_throw_id=%s;"
            parameters = (self._saving_throw_id,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._saving_throw_name=result[0]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_saving_throw_by_name(self):
        try:
            query = "SELECT saving_throw_id,saving_throw_name FROM saving_throw WHERE saving_throw_name=%s;"
            parameters = (self.saving_throw_name,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._saving_throw_id=result[0]
                self._saving_throw_name=result[1]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_saving_throw(self):
        try:
            query = "INSERT INTO saving_throw (saving_throw_name) VALUES (%s);"
            parameters = (str(self.saving_throw_name),)
            db = Db()
            await db.connection_db()
            self._saving_throw_id = await db.insert(query=query, parameters=parameters)
            return True
        except Exception as e:
            print(e)
            return False
        
    async def delete_saving_throw(self):
        try:
            query = "DELETE from saving_throw WHERE saving_throw_id=%s;"
            parameters = (self._saving_throw_id,)
            db = Db()
            await db.connection_db()
            return await db.delete(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False
        
    async def update_saving_throw(self,value):
        try:
            query = "UPDATE saving_throw SET saving_throw_name=%s WHERE saving_throw_id=%s"
            parameters = (value,self._saving_throw_id)
            db = Db()
            await db.connection_db()
            return await db.update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False        