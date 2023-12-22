from database import attributes
import pandas
import asyncio

from src import CharacterAttribute, Db, CharacterSavingThrow

class CharacterSkills(CharacterSavingThrow):
    def __init__(self, user_id=None,character_id=None):
        super().__init__(user_id=user_id, character_id=character_id)
        self._skills = [] 
        self._skills_from_attribute = []
        
    async def exists_skill(self, skill_id):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_skill_id FROM character_skill WHERE character_id = %s and skill_id = %s)"
                parameters = (self.character_id, skill_id,)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def insert_skill(self,skill_id):
        try:
            if self.character_id:
                query = "INSERT INTO character_skill(character_id,skill_id) VALUES(%s,%s) RETURNING character_skill_id;"
                parameters = (self.character_id,skill_id)
                db = Db()
                await db.connection_db()
                await db.insert(query=query, parameters=parameters)
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def delete_skills(self,skill_id):
        try:
            if self.character_id:
                query = """DELETE from character_skill
                WHERE skill_id=%s AND character_id=%s;"""
                parameters = (skill_id,self.character_id,)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
    
    async def load_skills(self):
        try:
            if self.character_id:
                query = """SELECT cs.skill_id, sk.skill_name, sk.usage_status, cs.character_skill_id 
                FROM character_skill cs 
                JOIN skill sk ON cs.skill_id = sk.skill_id 
                WHERE cs.character_id = %s;"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    self._skills.clear()
                    for row in result:
                        self._skills.append({'character_skill_id': row[3], 'skill_id': row[0], 'skill_name': row[1], 'usage_status': row[2]})
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def load_skills_attributes(self, usage_status):
        try:
            if self.character_id:
                query = """
                SELECT sk.skill_id, sk.skill_name, sk.usage_status, cs.character_skill_id AS id
                FROM skill sk
                LEFT JOIN character_skill cs ON cs.skill_id = sk.skill_id AND cs.character_id = %s
                WHERE sk.usage_status = %s;
                """
                parameters = (self.character_id, usage_status)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    self._skills_from_attribute.clear()
                    self._skills.clear()
                    for row in result:
                        self._skills_from_attribute.append({'skill_id': row[0], 'skill_name': row[1], 'usage_status': row[2]})
                        if row[3] is not None:
                            self._skills.append({'skill_name': row[1]})
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def update_skills(self,skill_id,character_skill_id):
        try:
            if self.character_id:
                query = """UPDATE character_skill
                SET skill_id=%s
                WHERE character_skill_id=%s;"""
                parameters = (skill_id,character_skill_id)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False

    async def get_skills(self,key):
        await self.load_skills()
        return getattr(self, key)
        
        
    @property
    def skills_name_list(self):
        lista = [d.get('skill_name') for d in self._skills]
        return lista if len(lista) > 0 else ''
    
    @property
    def skills_from_attribute(self):
        return self._skills_from_attribute

    @property
    def skill(self):
        return {
            'skills': {
                'acrobatics': self.acrobatics,
                'arcana': self.arcana,
                'athletics': self.athletics,
                'performance': self.performance,
                'deception': self.deception,
                'stealth': self.stealth,
                'history': self.history,
                'intimidation': self.intimidation,
                'insight': self.insight,
                'investigation': self.investigation,
                'animal_handling': self.animal_handling,
                'medicine': self.medicine,
                'nature': self.nature,
                'perception': self.perception,
                'persuasion': self.persuasion,
                'sleight_of_hand': self.sleight_of_hand,
                'religion': self.religion,
                'survival': self.survival
            },                
            'character_skills': self.skills_name_list
        }
    
    @property
    def skills(self):
        return self._skills
        
    @property
    def acrobatics(self):
        if any(d.get('skill_name') == 'acrobatics' for d in self.skills):
            return int(self.dexterity_bonus + self.proficiency_bonus) if self.dexterity_bonus is not None else int(self.proficiency_bonus)
        return int(self.dexterity_bonus) if self.dexterity_bonus is not None else ''

    @property
    def arcana(self):
        if any(d.get('skill_name') == 'arcana' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus) 
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def athletics(self):
        if any(d.get('skill_name') == 'athletics' for d in self.skills):
            return int(self.strength_bonus + self.proficiency_bonus) if self.strength_bonus is not None else int(self.proficiency_bonus)
        return int(self.strength_bonus) if self.strength_bonus is not None else ''

    @property
    def performance(self):
        if any(d.get('skill_name') == 'performance' for d in self.skills):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else ''

    @property
    def deception(self):
        if any(d.get('skill_name') == 'deception' for d in self.skills):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else ''

    @property
    def stealth(self):
        if any(d.get('skill_name') == 'stealth' for d in self.skills):
            return int(self.dexterity_bonus + self.proficiency_bonus) if self.dexterity_bonus is not None else int(self.proficiency_bonus)       
        return int(self.dexterity_bonus) if self.dexterity_bonus is not None else ''

    @property
    def history(self):
        if any(d.get('skill_name') == 'history' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def intimidation(self):
        if any(d.get('skill_name') == 'intimidation' for d in self.skills):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else ''

    @property
    def insight(self):
        if any(d.get('skill_name') == 'insight' for d in self.skills):
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''

    @property
    def investigation(self):
        if any(d.get('skill_name') == 'investigation' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def animal_handling(self):
        if any(d.get('skill_name') == 'animal_handling' for d in self.skills):
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''

    @property
    def medicine(self):
        if any(d.get('skill_name') == 'medicine' for d in self.skills):         
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''

    @property
    def nature(self):
        if any(d.get('skill_name') == 'nature' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def perception(self):
        if any(d.get('skill_name') == 'perception' for d in self.skills) :         
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''

    @property
    def persuasion(self):
        if any(d.get('skill_name') == 'persuasion' for d in self.skills):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else ''

    @property
    def sleight_of_hand(self):
        if any(d.get('skill_name') == 'sleight_of_hand' for d in self.skills):
            return int(self.dexterity_bonus + self.proficiency_bonus) if self.dexterity_bonus is not None else int(self.proficiency_bonus)       
        return int(self.dexterity_bonus) if self.dexterity_bonus is not None else ''

    @property
    def religion(self):
        if any(d.get('skill_name') == 'religion' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def survival(self):
        if any(d.get('skill_name') == 'survival' for d in self.skills):
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''