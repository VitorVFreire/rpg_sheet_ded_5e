from database import attributes
import pymysql
import asyncio

from src import Character, Db

class CharacterAttribute(Character):
    def __init__(self, user_id=None, character_id=None):
        super().__init__(user_id=user_id, character_id=character_id)
        self._attributes = {
            'strength': None,
            'dexterity': None,
            'intelligence': None,
            'constitution': None,
            'wisdom': None,
            'charisma': None
        }
        self._proficiency_bonus = None

    def check_value(self, value, key):
        value = int(value)
        key_possibility = ['strength', 'dexterity', 'intelligence', 'constitution', 'wisdom', 'charisma', 'proficiency_bonus']
        condition = 0 < value <= 30 if key != 'proficiency_bonus' else value >= 0
        return condition and key in key_possibility, key

    @property
    def attributes(self):
        return {
            'strength': self.strength,
            'strength_bonus': self.strength_bonus,
            'dexterity': self.dexterity,
            'dexterity_bonus': self.dexterity_bonus,
            'intelligence': self.intelligence,
            'intelligence_bonus': self.intelligence_bonus,
            'constitution': self.constitution,
            'constitution_bonus': self.constitution_bonus,
            'wisdom': self.wisdom,
            'wisdom_bonus': self.wisdom_bonus,
            'charisma': self.charisma,
            'charisma_bonus': self.charisma_bonus,
            'proficiency_bonus': self.external_proficiency_bonus
        }

    async def exists_attributes(self):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_attribute_id FROM character_attribute WHERE character_id = %s)"
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_attribute(self, key, value):
        try:
            condition, key = self.check_value(key=key, value=value)
            if self.character_id and condition:
                query = f"INSERT INTO character_attribute(character_id,{key}) VALUES(%s,%s) RETURNING character_attribute_id;;"
                parameters = (self.character_id, value,)
                db = Db()
                await db.connection_db()
                return (await db.insert(query=query, parameters=parameters) is not None)
            return False
        except Exception as e:
            print(e)
            return False

    async def delete_attributes(self):
        try:
            if self.character_id:
                query = """DELETE from character_attribute
                WHERE character_id=%s;"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False

    async def load_attributes(self):
        try:
            if self.character_id:
                query = """SELECT strength, dexterity, constitution, intelligence, wisdom, charisma,proficiency_bonus 
                FROM character_attribute WHERE character_id = %s"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters, all=False)
                if result:
                    self.set_strength(result[0])
                    self.set_dexterity(result[1])
                    self.set_constitution(result[2])
                    self.set_intelligence(result[3])
                    self.set_wisdom(result[4])
                    self.set_charisma(result[5])
                    self._proficiency_bonus = result[6]
                    return True
                return True
            return False
        except Exception as e:
            print(e)
            return False

    async def update_attributes(self, key, value):
        try:
            condition, key = self.check_value(key=key, value=value)
            if self.character_id and condition:
                query = f"""UPDATE character_attribute
                SET {key}=%s
                WHERE character_id=%s;"""
                parameters = (value, self.character_id)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False

    async def get_bonus(self, key):
        #await self.load_attributes()
        if key == 'proficiency_bonus':
            key = 'external_proficiency_bonus'
        else:
            key = f'{key}_bonus'
        return getattr(self, key)

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
        return int(self._attributes['strength']) if self._attributes['strength'] is not None else None

    @property
    def strength_bonus(self):
        return int(attributes.loc[self.strength]) if self.strength is not None else None

    def set_strength(self, value):
        self._attributes['strength'] = value

    @property
    def dexterity(self):
        return int(self._attributes['dexterity']) if self._attributes['dexterity'] is not None else None

    @property
    def dexterity_bonus(self):
        return int(attributes.loc[self.dexterity]) if self._attributes['dexterity'] is not None else None

    def set_dexterity(self, value):
        self._attributes['dexterity'] = value

    @property
    def constitution(self):
        return int(self._attributes['constitution']) if self._attributes['constitution'] is not None else None

    @property
    def constitution_bonus(self):
        return int(attributes.loc[self.constitution]) if self._attributes['constitution'] is not None else None

    def set_constitution(self, value):
        self._attributes['constitution'] = value

    @property
    def intelligence(self):
        return int(self._attributes['intelligence']) if self._attributes['intelligence'] is not None else None

    @property
    def intelligence_bonus(self):
        return int(attributes.loc[self.intelligence]) if self._attributes['intelligence'] is not None else None

    def set_intelligence(self, value):
        self._attributes['intelligence'] = value

    @property
    def wisdom(self):
        return int(self._attributes['wisdom']) if self._attributes['wisdom'] is not None else None

    @property
    def wisdom_bonus(self):
        return int(attributes.loc[self.wisdom]) if self._attributes['wisdom'] is not None else None

    def set_wisdom(self, value):
        self._attributes['wisdom'] = value

    @property
    def charisma(self):
        return int(self._attributes['charisma']) if self._attributes['charisma'] is not None else None

    @property
    def charisma_bonus(self):
        return int(attributes.loc[self.charisma]) if self._attributes['charisma'] is not None else None

    def set_charisma(self, value):
        self._attributes['charisma'] = value
