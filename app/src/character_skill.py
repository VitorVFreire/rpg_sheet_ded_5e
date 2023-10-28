from data import get_connection, attributes
import pandas
import pymysql
import asyncio

from src import CharacterAttribute

class CharacterSkills(CharacterAttribute):
    def __init__(self, id_user=None,id_character=None):
        super().__init__(id_user=id_user, id_character=id_character)
        self._skills = [] 
        
    async def exists_skill(self, id_pericia):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_pericia_personagem FROM pericia_personagem WHERE id_personagem = %s and id_pericia = %s)"
                        await mycursor.execute(query, (self.id_character, id_pericia,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def insert_skill(self,id_pericia):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO pericia_personagem(id_personagem,id_pericia) VALUES(%s,%s);"
                        await mycursor.execute(query, (self.id_character,id_pericia))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_skills(self,id_pericia):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from pericia_personagem
                        WHERE id_pericia=%s;"""
                        await mycursor.execute(query, (id_pericia,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def load_skills(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT pp.id_pericia, pc.nome_pericia, pc.status_uso,pp.id_pericia_personagem 
                        FROM pericia_personagem pp 
                        JOIN pericia pc ON pp.id_pericia = pc.id_pericia 
                        WHERE pp.id_personagem = %s;"""
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchall() 
                        if result:
                            self._skills.clear()
                            for row in result:
                                self._skills.append({'id_pericia_personagem': row[3], 'id_pericia': row[0], 'nome_pericia': row[1], 'status_uso': row[2]})
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_skills(self,id_pericia,id_pericia_personagem):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """UPDATE pericia_personagem
                        SET id_pericia=%s
                        WHERE id_pericia_personagem=%s;"""
                        await mycursor.execute(query, (id_pericia,id_pericia_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False

    async def get_skills(self,chave):
        await self.load_skills()
        return getattr(self, chave)
        
        
    @property
    def skills_name_list(self):
        lista = [d.get('nome_pericia') for d in self._skills]
        return lista if len(lista) > 0 else ''

    @property
    def skill(self):
        return {
            'pericias': {
                'acrobacia': self.acrobatics,
                'arcanismo': self.arcana,
                'atletismo': self.athletics,
                'atuacao': self.performance,
                'enganacao': self.deception,
                'furtividade': self.stealth,
                'historia': self.history,
                'intimidacao': self.intimidation,
                'intuicao': self.insight,
                'investigacao': self.investigation,
                'lidar_com_animais': self.animal_handling,
                'medicina': self.medicine,
                'natureza': self.nature,
                'percepcao': self.perception,
                'persuasao': self.persuasion,
                'prestidigitacao': self.sleight_of_hand,
                'religiao': self.religion,
                'sobrevivencia': self.survival
            },                
            'pericias_do_personagem': self.skills_name_list
        }
    
    @property
    def skills(self):
        return self._skills
        
    @property
    def acrobatics(self):
        if any(d.get('nome_pericia') == 'acrobacia' for d in self.skills):
            return int(self.dexterity_bonus + self.proficiency_bonus) if self.dexterity_bonus is not None else int(self.proficiency_bonus)
        return int(self.dexterity_bonus) if self.dexterity_bonus is not None else ''

    @property
    def arcana(self):
        if any(d.get('nome_pericia') == 'arcanismo' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus) 
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def athletics(self):
        if any(d.get('nome_pericia') == 'atletismo' for d in self.skills):
            return int(self.strength_bonus + self.proficiency_bonus) if self.strength_bonus is not None else int(self.proficiency_bonus)
        return int(self.strength_bonus) if self.strength_bonus is not None else ''

    @property
    def performance(self):
        if any(d.get('nome_pericia') == 'atuacao' for d in self.skills):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else ''

    @property
    def deception(self):
        if any(d.get('nome_pericia') == 'enganacao' for d in self.skills):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else ''

    @property
    def stealth(self):
        if any(d.get('nome_pericia') == 'furtividade' for d in self.skills):
            return int(self.dexterity_bonus + self.proficiency_bonus) if self.dexterity_bonus is not None else int(self.proficiency_bonus)       
        return int(self.dexterity_bonus) if self.dexterity_bonus is not None else ''

    @property
    def history(self):
        if any(d.get('nome_pericia') == 'historia' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def intimidation(self):
        if any(d.get('nome_pericia') == 'intimidacao' for d in self.skills):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else ''

    @property
    def insight(self):
        if any(d.get('nome_pericia') == 'intuicao' for d in self.skills):
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''

    @property
    def investigation(self):
        if any(d.get('nome_pericia') == 'investigacao' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def animal_handling(self):
        if any(d.get('nome_pericia') == 'lidar_com_animais' for d in self.skills):
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''

    @property
    def medicine(self):
        if any(d.get('nome_pericia') == 'medicina' for d in self.skills):         
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''

    @property
    def nature(self):
        if any(d.get('nome_pericia') == 'natureza' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def perception(self):
        if any(d.get('nome_pericia') == 'percepcao' for d in self.skills) :         
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''

    @property
    def persuasion(self):
        if any(d.get('nome_pericia') == 'persuasao' for d in self.skills):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else ''

    @property
    def sleight_of_hand(self):
        if any(d.get('nome_pericia') == 'prestidigitacao' for d in self.skills):
            return int(self.dexterity_bonus + self.proficiency_bonus) if self.dexterity_bonus is not None else int(self.proficiency_bonus)       
        return int(self.dexterity_bonus) if self.dexterity_bonus is not None else ''

    @property
    def religion(self):
        if any(d.get('nome_pericia') == 'religiao' for d in self.skills):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else ''

    @property
    def survival(self):
        if any(d.get('nome_pericia') == 'sobrevivencia' for d in self.skills):
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else ''