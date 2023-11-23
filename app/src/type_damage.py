import asyncio
from src import Db

class TypeDamage:
    def __init__(self,type_damage_id=None, type_damage_name=None):
        self._type_damage_id = type_damage_id or[]
        self._type_damage_name = type_damage_name or []
        
    @property
    def type_damage_name(self):
        return self._type_damage_name
    
    @property
    def type_damage_id(self):
        return self._type_damage_id
    
    @property
    async def types_damage(self):
        if (type(self._type_damage_id) is list and len(self._type_damage_id)<=0) or (self._type_damage_id is None):
            await self.load_types_damage()
        type_damages = []
        for type_damage_id, type_damage_name in zip(self._type_damage_id, self._type_damage_name):
            type_damages.append({'type_damage_id': type_damage_id, 'type_damage_name': type_damage_name})
        return type_damages
    
    async def load_types_damage(self):
        try:
            query = "SELECT type_damage_id, type_damage_name FROM type_damage;"
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                for row in result:
                    self._type_damage_id.append(row[0])
                    self._type_damage_name.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_type_damage(self):
        try:
            query = "SELECT type_damage_name FROM type_damage WHERE type_damage_id=%s;"
            parameters = (self._type_damage_id,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._type_damage_name=result[0]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_type_damage(self):
        try:
            query = "INSERT INTO type_damage (type_damage_name) VALUES (%s) RETURNING type_damage_id;"
            parameters = (str(self._type_damage_name),)
            db = Db()
            await db.connection_db()
            self._type_damage_id = await db.insert(query=query, parameters=parameters)
            return True
        except Exception as e:
            print(e)
            return False
        
    async def delete_type_damage(self):
        try:
            query = "DELETE from type_damage WHERE type_damage_id=%s;"
            parameters = (self._type_damage_id,)
            db = Db()
            await db.connection_db()
            return await db.delete(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False
        
    async def update_type_damage(self, value):
        try:
            query = "UPDATE type_damage SET type_damage_name=%s WHERE type_damage_id=%s;"
            parameters = (value, self._type_damage_id)
            db = Db()
            await db.connection_db()
            return await db.update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False   