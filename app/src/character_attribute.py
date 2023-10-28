from data import get_connection, attributes
import pymysql
import asyncio

from src import Character

class CharacterAttribute(Character):
    def __init__(self, id_user=None,id_character=None):
        super().__init__(id_user=id_user, id_character=id_character)
        self._attributes = {
            'forca': None,
            'destreza': None,
            'constituicao': None,
            'inteligencia': None,
            'sabedoria': None,
            'carisma': None
        }
        self._proficiency_bonus = None
        
    def check_value(self, value, key):
        value = int(value)
        key_possibility=['forca','destreza','constituicao','inteligencia','sabedoria','carisma','bonus_proficiencia' ]
        condition = 0 < value <= 30 if key != 'bonus_proficiencia' else value > 0
        return condition and key in key_possibility
        
    @property
    def attributes(self):
        return {
            'forca': self.strength,
            'bonus_forca': self.strength_bonus,
            'destreza': self.dexterity,
            'bonus_destreza': self.dexterity_bonus,
            'inteligencia': self.intelligence,
            'bonus_inteligencia': self.intelligence_bonus,
            'constituicao': self.constituition,
            'bonus_constituicao': self.constituition_bonus,
            'sabedoria': self.wisdom,
            'bonus_sabedoria': self.wisdom_bonus,
            'carisma': self.charisma,
            'bonus_carisma': self.charisma_bonus,
            'bonus_proficiencia': self.external_proficiency_bonus
        }
        
    async def exists_attributes(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_atributos FROM atributos WHERE id_personagem = %s)"
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def insert_attribute(self,key,value):
        try:
            if self.id_character and self.check_value(key=key, value=value):
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"INSERT INTO atributos(id_personagem,{key}) VALUES(%s,%s);"
                        await mycursor.execute(query, (self.id_character,value,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_attributes(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from atributos
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (self.id_character,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def load_attributes(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia 
                        FROM atributos WHERE id_personagem = %s"""
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchone() 
                        if result:
                            self.set_strength(result[0])
                            self.set_dexterity(result[1])
                            self.set_constituition(result[2])
                            self.set_intelligence(result[3])
                            self.set_wisdom(result[4])
                            self.set_charisma(result[5])
                            self._proficiency_bonus = result[6]
                            return True
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False

    
    async def update_attributes(self, key, value):
        try:
            if self.id_character and self.check_value(key=key, value=value):
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE atributos
                        SET {key}=%s
                        WHERE id_personagem=%s;"""
                        parametros=(value,self.id_character)
                        await mycursor.execute(query, parametros)
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def get_bonus(self, key):
        await self.load_attributes()
        if key == 'bonus_proficiencia':
            key = 'proficiencia_externa'
        return getattr(self, f'bonus_{key}')
        
    @property
    def proficiency_bonus(self):
        return int(self._proficiency_bonus) if self._proficiency_bonus is not None else 0
    
    @property
    def external_proficiency_bonus(self):
        return int(self._proficiency_bonus) if self._proficiency_bonus is not None else 0
    
    @proficiency_bonus.setter
    def proficiency_bonus(self, value):
        self._proficiency_bonus = value
    
    @property
    def strength(self):
        return int(self._attributes['forca']) if self._attributes['forca'] is not None else None
    
    @property
    def strength_bonus(self):
        return int(attributes.loc[self.strength]) if self.strength is not None else None
    
    def set_strength(self, value):
        self._attributes['forca'] = value 
        
    @property
    def dexterity(self):
        return int(self._attributes['destreza']) if self._attributes['destreza'] is not None else None
    
    @property
    def dexterity_bonus(self):
        return int(attributes.loc[self.dexterity]) if self._attributes['destreza'] is not None else None
    
    def set_dexterity(self,value):
        self._attributes['destreza'] = value
    
    @property
    def constituition(self):
        return int(self._attributes['constituicao']) if self._attributes['constituicao'] is not None else None
    
    @property
    def constituition_bonus(self):
        return int(attributes.loc[self.constituition]) if self._attributes['constituicao'] is not None else None
           
    def set_constituition(self,value):
        self._attributes['constituicao'] = value
    
    @property
    def intelligence(self):
        return int(self._attributes['inteligencia']) if self._attributes['inteligencia'] is not None else None
    
    @property
    def intelligence_bonus(self):
        return int(attributes.loc[self.intelligence]) if self._attributes['inteligencia'] is not None else None
    
    def set_intelligence(self,value):
        self._attributes['inteligencia'] = value
    
    @property
    def wisdom(self):
        return int(self._attributes['sabedoria']) if self._attributes['sabedoria'] is not None else None
    
    @property
    def wisdom_bonus(self):
        return int(attributes.loc[self.wisdom]) if self._attributes['sabedoria'] is not None else None
     
    def set_wisdom(self,value):
        self._attributes['sabedoria'] = value
    
    @property
    def charisma(self):
        return int(self._attributes['carisma']) if self._attributes['carisma'] is not None else None
    
    @property
    def charisma_bonus(self):
        return int(attributes.loc[self.charisma]) if self._attributes['carisma'] is not None else None
    
    def set_charisma(self,value):
        self._attributes['carisma'] = value