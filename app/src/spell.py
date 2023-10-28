from data import get_connection
import pymysql
import asyncio

class Spell:
    def __init__(self, id_spell = None, attribute_name = None, sides_dices = None, link_details = None, spell_name = None, damege_type = None, amount_dices = None, level_spell = None, additional_per_level = None):
        self._id_spell = id_spell or []
        self._attribute_name = attribute_name or []
        self._spell_name = spell_name or []
        self._level_spell = level_spell or []
        self._damege_type = damege_type or []
        self._amount_dices = amount_dices or []
        self._sides_dices = sides_dices or []
        self._additional_per_level = additional_per_level or [] 
        self._link_details = link_details or []
        self.__character_spell = []
        
    async def load_character_spells(self, id_character):
        try:
            if id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT id_habilidade FROM habilidade_personagem WHERE id_personagem = %s;"""
                        await mycursor.execute(query, id_character)
                        result = await mycursor.fetchall()
                        if result:
                            for row in result:
                                self.__character_spell.append(row[0])              
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    async def spells(self):
        if (type(self._id_spell) is list and len(self._id_spell)<=0) or (self._id_spell is None):
            await self.load_spells()
        spells = []
        for id_spell, attribute_name, spell_name, level_spell, damege_type, amount_dices, sides_dices, additional_per_level, link_details in zip(self._id_spell, self._attribute_name, self._spell_name, self._level_spell, self._damege_type, self._amount_dices, self._sides_dices, self._additional_per_level, self._link_details):
            spells.append({
                'id_habilidade': id_spell, 
                'nome_atributo': attribute_name, 
                'nome_habilidade': spell_name, 
                'nivel_habilidade': level_spell, 
                'tipo_dano': damege_type, 
                'qtd_dados': amount_dices, 
                'lados_dados': sides_dices, 
                'adicional_por_nivel': additional_per_level, 
                'link_detalhes': link_details,
                'personagem_possui': id_spell in self.__character_spell
            })
        return spells
    
    @property
    async def spell(self):
        if self._id_spell is None:
            await self.load_spell()
        spell = {
            'id_habilidade': self.id_spell, 
            'nome_atributo': self.attribute_name, 
            'nome_habilidade': self.spell_name, 
            'nivel_habilidade': self.level_spell, 
            'tipo_dano': self.damege_type, 
            'qtd_dados': self.amount_dices, 
            'lados_dados': self.sides_dices, 
            'adicional_por_nivel': self.additional_per_level, 
            'link_detalhes': self.link_details
        }
        return spell
   
    async def load_spells(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_habilidade, nome_atributo, nome_habilidade, nivel_habilidade, tipo_dano, qtd_dados, lados_dados, adicional_por_nivel, link_detalhes FROM habilidade;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        for row in result:
                            self._id_spell.append(row[0])
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
                    query = "SELECT id_habilidade, nome_atributo, nome_habilidade, nivel_habilidade, tipo_dano, qtd_dados, lados_dados, adicional_por_nivel, link_detalhes FROM habilidade WHERE id_habilidade=%s;"
                    await mycursor.execute(query,(self._id_spell,))
                    result = await mycursor.fetchone() 
                    if result:
                        self._id_spell = result[0]
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
                    query = "INSERT INTO habilidade (nome_atributo, nome_habilidade, nivel_habilidade, tipo_dano, qtd_dados, lados_dados, adicional_por_nivel, link_detalhes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
                    await mycursor.execute(query, (self.attribute_name, self.spell_name, self.level_spell, self.damege_type, self.amount_dices, self.sides_dices, self.additional_per_level, self.link_details))
                    self.id_habilidaded_habilidade = mycursor.lastrowid   
                    await conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            return False

    async def delete_spell(self):
        try:
            if self._id_spell:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from habilidade
                        WHERE id_habilidade=%s;"""
                        await mycursor.execute(query, (self._id_spell,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_spell(self, key, value):
        try:
            possible_key = ['id_habilidade', 'nome_atributo', 'nome_habilidade', 'nivel_habilidade', 'tipo_dano', 'qtd_dados', 'lados_dados', 'adicional_por_nivel', 'link_detalhes']
            if key in possible_key:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE habilidade SET {key}=%s WHERE id_habilidade=%s"""
                        await mycursor.execute(query, (value, self._id_spell))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
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
    def id_spell(self):
        return self._id_spell
    
    @id_spell.setter
    def id_spell(self, value):
        self._id_spell = value
        
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