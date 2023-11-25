import asyncio
from src import Db

class KindEquipment:
    def __init__(self,kind_equipment_id=None, kind_equipment_name=None):
        self._kind_equipment_id = kind_equipment_id or[]
        self._kind_equipment_name = kind_equipment_name or []
        
    @property
    def kind_equipment_name(self):
        return self._kind_equipment_name
    
    @property
    def kind_equipment_id(self):
        return self._kind_equipment_id
    
    @property
    async def kind_equipments(self):
        if (type(self._kind_equipment_id) is list and len(self._kind_equipment_id)<=0) or (self._kind_equipment_id is None):
            await self.load_kind_equipments()
        kind_equipments = []
        for kind_equipment_id, kind_equipment_name in zip(self._kind_equipment_id, self._kind_equipment_name):
            kind_equipments.append({'kind_equipment_id': kind_equipment_id, 'kind_equipment_name': kind_equipment_name})
        return kind_equipments
    
    async def load_kind_equipments(self):
        try:
            query = "SELECT kind_equipment_id, kind_equipment_name FROM kind_equipment;"
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                for row in result:
                    self._kind_equipment_id.append(row[0])
                    self._kind_equipment_name.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_kind_equipment(self):
        try:
            query = "SELECT kind_equipment_name FROM kind_equipment WHERE kind_equipment_id=%s;"
            parameters = (self._kind_equipment_id,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._kind_equipment_name=result[0]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_kind_equipment_with_name(self):
        try:
            query = "SELECT kind_equipment_id FROM kind_equipment WHERE kind_equipment_name=%s;"
            parameters = (self._kind_equipment_name,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._kind_equipment_id=result[0]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_kind_equipment(self):
        try:
            query = "INSERT INTO kind_equipment (kind_equipment_name) VALUES (%s) RETURNING kind_equipment_id;"
            parameters = (str(self._kind_equipment_name),)
            db = Db()
            await db.connection_db()
            self._kind_equipment_id = await db.insert(query=query, parameters=parameters)
            return True
        except Exception as e:
            print(e)
            return False
        
    async def delete_kind_equipment(self):
        try:
            query = "DELETE from kind_equipment WHERE kind_equipment_id=%s;"
            parameters = (self._kind_equipment_id,)
            db = Db()
            await db.connection_db()
            return await db.delete(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False
        
    async def update_kind_equipment(self, value):
        try:
            query = "UPDATE kind_equipment SET kind_equipment_name=%s WHERE kind_equipment_id=%s;"
            parameters = (value, self._kind_equipment_id)
            db = Db()
            await db.connection_db()
            return await db.update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False  