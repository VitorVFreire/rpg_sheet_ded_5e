import asyncio

from src import Db

class Skill:
    def __init__(self,skill_id=None,skill_name=None,usage_status=None):
        self._skill_id = skill_id or []
        self._skill_name = skill_name or []
        self._usage_status = usage_status or []
        
    @property
    def skill_name(self):
        return self._skill_name
    
    @property
    def skill_id(self):
        return self._skill_id
    
    @property
    def usage_status(self):
        return self._usage_status
    
    @property
    async def skills(self):
        if (type(self._skill_id) is list and len(self._skill_id)<=0) or (self._skill_id is None):
            await self.load_skills()
        skills=[]
        for skill_id, skill_name, usage_status in zip(self._skill_id,self._skill_name,self._usage_status):
            skills.append({'skill_id ': skill_id, 'skill_name': skill_name, 'usage_status': usage_status})
        return skills
    
    async def load_skills(self):
        try:
            query = "SELECT skill_id, skill_name, usage_status FROM skill;"
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                for row in result:
                    self._skill_id.append(row[0])
                    self._skill_name.append(row[1])
                    self._usage_status.append(row[2])
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_skill(self):
        try:
            query = "SELECT skill_name, usage_status FROM skill WHERE skill_id =%s;"
            parameters = (self._skill_id,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._skill_name=result[0]
                self._usage_status=result[1]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_skill_by_name(self):
        try:
            query = "SELECT skill_id , usage_status FROM skill WHERE skill_name=%s;"
            parameters = (self.skill_name,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._skill_id=result[0]
                self._usage_status=result[1]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_skill(self):
        try:
            query = "INSERT INTO skill(skill_name,usage_status) VALUES(%s,%s) RETURNING skill_id;"
            parameters = (self._skill_name,self._usage_status,)
            db = Db()
            await db.connection_db()
            self._skill_id = await db.insert(query=query, parameters=parameters)
            return True
        except Exception as e:
            print(e)
            return False
        
    async def delete_skill(self):
        try:
            query = """DELETE from skill
            WHERE skill_id =%s;"""
            parameters = (self._skill_id,)
            db = Db()
            await db.connection_db()
            return await db.delete(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            return False
        
    async def update_skill(self,key,value):
        try:
            possiveis_key=['skill_name','usage_status']
            if key in possiveis_key:
                query = f"UPDATE skill SET {key}=%s WHERE skill_id =%s"
                parameters = (value,self._skill_id,)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False        