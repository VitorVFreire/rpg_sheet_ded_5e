from data import get_connection
import pymysql
import asyncio

class Skill:
    def __init__(self,id_skill=None,skill_name=None,usage_status=None):
        self._id_skill = id_skill or []
        self._skill_name = skill_name or []
        self._usage_status = usage_status or []
        
    @property
    def skill_name(self):
        list = {
            'acrobatics': 'acrobacia',
            'arcana': 'arcanismo',
            'athletics': 'atletismo',
            'performance': 'atuacao',
            'deception': 'enganacao',
            'stealth': 'furtividade',
            'history': 'historia',
            'intimidation': 'intimidacao',
            'insight': 'intuicao',
            'investigation': 'investigacao',
            'animal_handling': 'lidar_com_animais',
            'medicine': 'medicina',
            'nature': 'natureza',
            'perception': 'percepcao',
            'persuasion': 'persuasao',
            'sleight_of_hand': 'prestidigitacao',
            'religion': 'religiao',
            'survival': 'sobrevivencia'
        }
        return list[self._skill_name]
    
    @property
    def id_skill(self):
        return self._id_skill
    
    @property
    def usage_status(self):
        return self._usage_status
    
    @property
    async def skills(self):
        if (type(self._id_skill) is list and len(self._id_skill)<=0) or (self._id_skill is None):
            await self.load_skills()
        pericias=[]
        for id_pericia,nome_pericia,status_uso in zip(self._id_skill,self._skill_name,self._usage_status):
            pericias.append({'id_pericia':id_pericia,'nome_pericia':nome_pericia,'status_uso':status_uso})
        return pericias
    
    async def load_skills(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT id_pericia, nome_pericia, status_uso from pericia;"
                        await mycursor.execute(query)
                        result = await mycursor.fetchall() 
                        if result:
                            for row in result:
                                self._id_skill.append(row[0])
                                self._skill_name.append(row[1])
                                self._usage_status.append(row[2])
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_skill(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT nome_pericia, status_uso FROM pericia WHERE id_pericia=%s;"
                        await mycursor.execute(query,(self._id_skill,))
                        result = await mycursor.fetchall() 
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
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT id_pericia, status_uso FROM pericia WHERE nome_pericia=%s;"
                        await mycursor.execute(query,(self.skill_name,))
                        result = await mycursor.fetchone() 
                        if result:
                            self._id_skill=result[0]
                            self._usage_status=result[1]
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_skill(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO pericia(nome_pericia,status_uso) VALUES(%s,%s);"
                        await mycursor.execute(query, (self._skill_name,self._usage_status,))
                        self._id_skill = mycursor.lastrowid
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_skill(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from pericia
                        WHERE id_pericia=%s;"""
                        await mycursor.execute(query, (self._id_skill,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_skill(self,key,value):
        try:
            possiveis_key=['nome_pericia','status_uso']
            if key in possiveis_key:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"UPDATE pericia SET {key}=%s WHERE id_pericia=%s"
                        await mycursor.execute(query, (value,self._id_skill,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False        