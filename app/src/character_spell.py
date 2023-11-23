import asyncio

from src import Character, Db

class CharacterSpell(Character):
    def __init__(self, user_id=None, character_id=None):
        super().__init__(user_id=user_id, character_id=character_id)
        self._spells = []
    
    async def exists_specific_spell(self, spell_id):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_spell_id FROM character_spell WHERE spell_id = %s and character_id = %s)"
                parameters = (spell_id,self.character_id,)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def exists_spell(self):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_spell_id FROM character_spell WHERE character_id = %s)"
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def insert_spell(self,spell_id):
        try:
            if self.character_id:
                query = "INSERT INTO character_spell(character_id,spell_id) VALUES(%s,%s) RETURNING spell_id;"
                parameters = (self.character_id,spell_id)
                db = Db()
                await db.connection_db()
                await db.insert(query=query, parameters=parameters)
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def update_spell(self,spell_id,character_id_spell):
        try:
            if self.character_id:
                query = """UPDATE character_spell
                SET spell_id=%s
                WHERE character_spell_id=%s;"""
                parameters = (spell_id,character_id_spell)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False    
        
    async def delete_spell(self,character_id_spell):
        try:
            if self.character_id:
                query = """DELETE from character_spell
                WHERE spell_id=%s and character_id = %s;"""
                parameters = (character_id_spell, self.character_id)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_spells(self):
        try:
            if self.character_id:
                query = """SELECT sp.spell_id, sp.spell_name, sp.attribute_use, sp.spell_level, tp.type_damage_name, sp.amount_dice, sp.side_dice, sp.add_per_level, sp.description_spell, cs.character_spell_id
                FROM character_spell cs
                JOIN spell sp ON cs.spell_id = sp.spell_id
                JOIN type_damage tp ON sp.type_damage_id = tp.type_damaga_id
                WHERE cs.character_id = %s;"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    for row in result:
                        spell = {
                            'spell_id': row[0],
                            'spell_name': row[1],
                            'attribute_use': row[2],
                            'spell_level': row[3],
                            'tipo_dano': row[4],
                            'amount_dice': row[5],
                            'side_dice': row[6],
                            'add_per_level': row[7],
                            'description_spell': row[8],
                            'character_spell_id': row[9]
                        }
                        self.spell = spell              
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    @property
    def spell(self, value):
        return self._spells[value]
    
    @property
    def spells(self):
        return self._spells  
    
    @spell.setter
    def spell(self,value):
        self._spells.append(value)