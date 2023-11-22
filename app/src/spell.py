import asyncio
from src import Db

class Spell:
    def __init__(self, spell_id = None, attribute_name = None, sides_dices = None, link_details = None, spell_name = None, damege_type = None, amount_dices = None, level_spell = None, additional_per_level = None):
        self._spell_id = spell_id or []
        self._attribute_name = attribute_name or []
        self._spell_name = spell_name or []
        self._level_spell = level_spell or []
        self._damege_type = damege_type or []
        self._amount_dices = amount_dices or []
        self._sides_dices = sides_dices or []
        self._additional_per_level = additional_per_level or [] 
        self._link_details = link_details or []
        self.__character_spell = []
        
    async def load_character_spells(self, character_id):
        try:
            if character_id:
                query = "SELECT spell_id FROM habilidade_personagem WHERE id_personagem = %s;"
                parameters = (character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    for row in result:
                        self.__character_spell.append(row[0])              
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    @property
    async def spells(self):
        if (type(self._spell_id) is list and len(self._spell_id)<=0) or (self._spell_id is None):
            await self.load_spells()
        spells = []
        for spell_id, attribute_name, spell_name, level_spell, damege_type, amount_dices, sides_dices, additional_per_level, link_details in zip(self._spell_id, self._attribute_name, self._spell_name, self._level_spell, self._damege_type, self._amount_dices, self._sides_dices, self._additional_per_level, self._link_details):
            spells.append({
                'spell_id': spell_id, 
                'attribute_name': attribute_name, 
                'spell_name': spell_name, 
                'lelvel_spell': level_spell, 
                'damege_type': damege_type, 
                'amount_dices': amount_dices, 
                'sides_dices': sides_dices, 
                'additional_per_level': additional_per_level, 
                'link_details': link_details,
                'personagem_possui': spell_id in self.__character_spell
            })
        return spells
    
    @property
    async def spell(self):
        if self._spell_id is None:
            await self.load_spell()
        spell = {
            'spell_id': self.spell_id, 
            'attribute_name': self.attribute_name, 
            'spell_name': self.spell_name, 
            'lelvel_spell': self.level_spell, 
            'damege_type': self.damege_type, 
            'amount_dices': self.amount_dices, 
            'sides_dices': self.sides_dices, 
            'additional_per_level': self.additional_per_level, 
            'link_details': self.link_details
        }
        return spell
   
    async def load_spells(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT spell_id, nome_atributo, spell_name, lelvel_spell, damege_type, amount_dices, sides_dices, additional_per_level, link_details FROM habilidade;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        for row in result:
                            self._spell_id.append(row[0])
                            self._attribute_name.append(row[1])
                            self._spell_name.append(row[2])
                            self._level_spell.append(row[3])
                            self._damege_type.append(row[4])
                            self._amount_dices.append(row[5])
                            self._sides_dices.append(row[6])
                            self._additional_per_level.append(row[7])
                            self._link_details.append(row[8])
                        return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def load_spell(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT spell_id, nome_atributo, spell_name, lelvel_spell, damege_type, amount_dices, sides_dices, additional_per_level, link_details FROM habilidade WHERE spell_id=%s;"
                    await mycursor.execute(query,(self._spell_id,))
                    result = await mycursor.fetchone() 
                    if result:
                        self._spell_id = result[0]
                        self._attribute_name = result[1]
                        self._spell_name = result[2]
                        self._level_spell = result[3]
                        self._damege_type = result[4]
                        self._amount_dices = result[5]
                        self._sides_dices = result[6]
                        self._additional_per_level = result[7]
                        self._link_details = result[8]
                        return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_spell(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "INSERT INTO habilidade (nome_atributo, spell_name, lelvel_spell, damege_type, amount_dices, sides_dices, additional_per_level, link_details) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
                    await mycursor.execute(query, (self.attribute_name, self.spell_name, self.level_spell, self.damege_type, self.amount_dices, self.sides_dices, self.additional_per_level, self.link_details))
                    self.spell_idd_habilidade = mycursor.lastrowid   
                    await conn.commit()
                    return True
        except Exception as e:
            print(e)
            return False

    async def delete_spell(self):
        try:
            if self._spell_id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from habilidade
                        WHERE spell_id=%s;"""
                        await mycursor.execute(query, (self._spell_id,))
                        await conn.commit()
                        return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def update_spell(self, key, value):
        try:
            possible_key = ['spell_id', 'nome_atributo', 'spell_name', 'lelvel_spell', 'damege_type', 'amount_dices', 'sides_dices', 'additional_per_level', 'link_details']
            if key in possible_key:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE habilidade SET {key}=%s WHERE spell_id=%s"""
                        await mycursor.execute(query, (value, self._spell_id))
                        await conn.commit()
                        return True
            return False
        except Exception as e:
            print(e)
            return False 
        
    @property
    def spell_name(self):
        return self._spell_name
    
    @spell_name.setter
    def spell_name(self, value):
        self._spell_name = value
        
    @property
    def attribute_name(self):
        return self._attribute_name
    
    @attribute_name.setter
    def attribute_name(self, value):
        self._attribute_name = value
    
    @property
    def spell_id(self):
        return self._spell_id
    
    @spell_id.setter
    def spell_id(self, value):
        self._spell_id = value
        
    @property
    def damege_type(self):
        return self._damege_type
    
    @damege_type.setter
    def damege_type(self, value):
        self._damege_type = value
        
    @property
    def amount_dices(self):
        return self._amount_dices
    
    @amount_dices.setter
    def amount_dices(self, value):
        self._amount_dices = value 
    
    @property
    def sides_dices(self):
        return self._sides_dices
    
    @sides_dices.setter
    def sides_dices(self, value):
        self._sides_dices = value
        
    @property
    def additional_per_level(self):
        return self._additional_per_level
    
    @additional_per_level.setter
    def additional_per_level(self, value):
        self._additional_per_level = value
        
    @property
    def link_details(self):
        return self._link_details
    
    @link_details.setter
    def link_details(self, value):
        self._link_details = value
        
    @property
    def level_spell(self):
        return self._level_spell
    
    @level_spell.setter
    def level_spell(self, value):
        self._level_spell = value