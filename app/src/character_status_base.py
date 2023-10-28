from data import get_connection
import pymysql
import asyncio

from src import Character

class CharacterStatusBase(Character):
    def __init__(self, id_user=None,id_character=None):
        super().__init__(id_user=id_user, id_character=id_character)
        self._alignment = None
        self._antecedent = None
        self._ca = None
        self._displacement = None
        self._faction = None
        self._inspiration = None
        self._initiative = None
        self._level = None
        self._life = None
        self._current_life = None
        self._temporary_life = None
        self._xp = None
    
    def valid_key(self, key):
        possible_keys=['vida','xp','nivel','alinhamento','antecendente','faccao','inspiracao','ca','iniciativa','deslocamento','vida_atual','vida_temporaria']
        return key in possible_keys
        
    async def exists_status_base(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_status_base FROM status_base WHERE id_personagem = %s)"
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def insert_status_base(self,key,value):
        try:
            if self.id_character and self.valid_key(key):
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"INSERT INTO status_base(id_personagem,{key}) VALUES(%s,%s);"
                        await mycursor.execute(query, (self.id_character,value,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_status_base(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from status_base
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (self.id_character))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def load_status_base(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT vida,xp,nivel,alinhamento,antecendente,faccao,inspiracao,ca,iniciativa,deslocamento,vida_atual,vida_temporaria
                        FROM status_base
                        WHERE id_personagem = %s;"""
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchone()
                        if result:
                            self.life = result[0]
                            self.xp = result[1]
                            self.level = result[2]
                            self.alignment = result[3] 
                            self.antecedent = result[4] 
                            self.faction = result[5]  
                            self.inspiration = result[6]
                            self.ca = result[7]
                            self.initiative = result[8]
                            self.displacement = result[9]
                            self.current_life = result[10]
                            self.temporary_life = result[11]     
                            return True
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_status_base(self,key,value):
        try:
            if self.id_character and self.valid_key(key):
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE status_base
                        SET {key}=%s
                        WHERE id_personagem=%s;"""
                        parameters = (value,self.id_character)
                        await mycursor.execute(query, parameters)
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    @property
    def status_base(self):
        return {
            'nivel': self.level,
            'alinhamento': self.alignment,
            'faccao': self.faction,
            'antecendente': self.antecedent,
            'xp': self.xp,
            'deslocamento': self.displacement,
            'iniciativa': self.initiative,
            'vida': self.life,
            'vida_atual': self.current_life,
            'vida_temporaria': self.temporary_life,
            'inspiracao': self.inspiration,
            'ca': self.ca
        }
    
    @property
    def level(self):
        return int(self._level) if self._level is not None else None 
    
    @level.setter
    def level(self,value):
        self._level=value
    
    @property
    def alignment(self):
        return self._alignment
    
    @alignment.setter
    def alignment(self,value):
        self._alignment=value
        
    @property
    def faction(self):
        return self._faction        
         
    @faction.setter
    def faction(self,value):
        self._faction=value
        
    @property
    def antecedent(self):
        return self._antecedent        
         
    @antecedent.setter
    def antecedent(self,value):
        self._antecedent=value
    
    @property
    def xp(self):
        return self._xp
                
    @xp.setter
    def xp(self,value):
        self._xp=value
           
    @property
    def displacement(self):
        return self._displacement
    
    @displacement.setter
    def displacement(self,value):
        self._displacement=value
        
    @property
    def initiative(self):
        return self._initiative
    
    @initiative.setter
    def initiative(self,value):
        self._initiative=value
    
    @property
    def life(self):
        return self._life
    
    @life.setter
    def life(self,value):
        self._life=value
        
    @property
    def current_life(self):
        return self._current_life
    
    @current_life.setter
    def current_life(self,value):
        self._current_life=value
       
    @property
    def temporary_life(self):
        return self._temporary_life
    
    @temporary_life.setter
    def temporary_life(self,value):
        self._temporary_life=value
        
    @property
    def inspiration(self):
        return self._inspiration
    
    @inspiration.setter
    def inspiration(self,value):
        self._inspiration=value
    
    @property
    def ca(self):
        return self._ca
    
    @ca.setter
    def ca(self,value):
        self._ca=value