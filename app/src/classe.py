import asyncio

from src import Db

class Classe:
    def __init__(self, class_id=None, class_name=None):
        self._class_id = class_id or []
        self._class_name = class_name or []
        
    @property
    def class_name(self):
        return self._class_name
    
    @property
    def class_id(self):
        return self._class_id

    @property
    async def classes(self):
        if (type(self._class_id) is list and len(self._class_id)<=0) or (self._class_id is None):
            await self.load_classes()
        classes=[]
        for class_id, class_name in zip(self._class_id, self._class_name):
            classes.append({'class_id': class_id, 'class_name': class_name})
        return classes
    
    async def load_classes(self):
        try:
            query = "SELECT class_id, class_name FROM class;"
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                for row in result:
                    self._class_id.append(row[0])
                    self._class_name.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def load_class(self):
        try:
            query = "SELECT class_name FROM class WHERE class_id=%s;"
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=(self._class_id,), all=False) 
            if result:
                self._class_name=result[0]
                return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_class(self):
        try:
            query = "INSERT INTO classe (nome_classe) VALUES (%s);"
            parameters = (str(self._class_name),)
            db = Db()
            await db.connection_db()
            self._class_id = await db.insert(query=query, parameters=parameters) 
            return True
        except Exception as e:
            print(e)
            return False

    async def delete_class(self):
        try:
            query = """DELETE from classe
            WHERE class_id=%s;"""
            parameters = (self._class_id,)
            db = Db()
            await db.connection_db()
            return await db.delete(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False
        
    async def update_class(self, value):
        try:
            query = "UPDATE classe SET nome_classe=%s WHERE class_id=%s"
            parameters = (value,self._class_id)
            db = Db()
            await db.connection_db()
            return await db.update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False 