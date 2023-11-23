from data import attributes
import asyncio

from src import CharacterAttribute, Db

class CharacterSavingThrowTest(CharacterAttribute):
    def __init__(self, user_id=None,character_id=None):
        super().__init__(user_id=user_id, character_id=character_id)
        self._saving_throws = []
    
    async def exists_saving_throw(self, saving_throw_id):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_saving_throw_id FROM character_saving_throw WHERE character_id = %s and saving_throw_id = %s)"
                parameters = (self.character_id, saving_throw_id)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_saving_throws(self, saving_throw_id):
        try:
            if self.character_id:
                query = """
                    INSERT INTO character_saving_throw 
                    (character_id, saving_throw_id)
                    VALUES (%s, %s) RETURNING character_saving_throw_id;
                """
                parameters = (self.character_id,saving_throw_id,)
                db = Db()
                await db.connection_db()
                await db.insert(query=query, parameters=parameters)
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def delete_saving_throw(self, saving_throw_id):
        try:
            if self.character_id:
                query = """DELETE from character_saving_throw
                WHERE saving_throw_id=%s;"""
                parameters = (saving_throw_id,)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
    
    async def load_saving_throws(self):
        try:
            if self.character_id:
                query = """SELECT st.saving_throw_id, st.saving_throw_name, cs.character_saving_throw_id 
                FROM character_saving_throw cs, saving_throw st 
                WHERE cs.character_id = %s and st.saving_throw_id=cs.saving_throw_id"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    self._saving_throws.clear()
                    for row in result:
                        self._saving_throws.append({'character_saving_throw_id': row[2], 'saving_throw_id': row[0],'saving_throw_name': row[1]})
                    return True
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def update_saving_throw(self, new_saving_throw_id, last_saving_throw_id):
        try:
            if self.character_id:
                query = """UPDATE character_saving_throw
                SET saving_throw_id=%s
                WHERE saving_throw_id=%s;"""
                await mycursor.execute(query, (new_saving_throw_id, last_saving_throw_id,))
                parameters = (saving_throw_id,)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def get_saving_throws(self,key):
        await self.load_saving_throws()
        return getattr(self, key)
        
    @property
    def saving_throws(self):
        return {
            'strength_resistance': self.strength_resistance,
            'dexterity_resistance': self.dexterity_resistance,
            'intelligence_resistance': self.intelligence_resistance,
            'constitution_resistance': self.constitution_resistance,
            'wisdom_resistance': self.wisdom_resistance,
            'charisma_resistance': self.charisma_resistance,
            'saving_throw_name_list': self.saving_throw_name_list
        }
        
    @property
    def saving_throw_name_list(self):
        lista = [f"{d.get('saving_throw_name')}_resistance" for d in self._saving_throws]
        return lista

    @property
    def strength_resistance(self):
        if any(d.get('saving_throw_name') == 'strength' for d in self._saving_throws):
            return int(self.strength_bonus + self.proficiency_bonus) if self.strength_bonus is not None else int(self.proficiency_bonus)
        return int(self.strength_bonus) if self.strength_bonus is not None else None
    
    @property
    def dexterity_resistance(self):
        if any(d.get('saving_throw_name') == 'dexterity' for d in self._saving_throws):
            return int(self.dexterity_bonus + self.proficiency_bonus) if self.dexterity_bonus is not None else int(self.proficiency_bonus)
        return int(self.dexterity_bonus) if self.dexterity_bonus is not None else None
    
    @property
    def constitution_resistance(self):
        if any(d.get('saving_throw_name') == 'constitution' for d in self._saving_throws):
            return int(self.constitution_bonus + self.proficiency_bonus) if self.constitution_bonus is not None else int(self.proficiency_bonus)
        return int(self.constitution_bonus) if self.constitution_bonus is not None else None
    
    @property
    def intelligence_resistance(self):
        if any(d.get('saving_throw_name') == 'intelligence' for d in self._saving_throws):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else None
    
    @property
    def wisdom_resistance(self):
        if any(d.get('saving_throw_name') == 'wisdom' for d in self._saving_throws):
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else None
    
    @property
    def charisma_resistance(self):
        if any(d.get('saving_throw_name') == 'charisma' for d in self._saving_throws):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else None