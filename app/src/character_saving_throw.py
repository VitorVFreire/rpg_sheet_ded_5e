from data import get_connection, attributes
import pymysql
import asyncio

from src import CharacterAttribute

class CharacterSavingThrow(CharacterAttribute):
    def __init__(self, id_user=None,id_character=None):
        super().__init__(id_user=id_user, id_character=id_character)
        self._saving_throws = []
    
    async def exists_saving_throw(self, id_saving_throw):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_salvaguarda_personagem FROM salvaguarda_personagem WHERE id_personagem = %s and id_salvaguarda = %s)"
                        await mycursor.execute(query, (self.id_character, id_saving_throw))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def insert_saving_throws(self,id_saving_throw):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """
                            INSERT INTO `RPG`.`salvaguarda_personagem` 
                            (`id_personagem`, `id_salvaguarda`)
                            VALUES (%s, %s)
                        """
                        await mycursor.execute(query, (self.id_character,id_saving_throw,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def delete_saving_throw(self,id_saving_throw):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from salvaguarda_personagem
                        WHERE id_salvaguarda=%s;"""
                        await mycursor.execute(query, (id_saving_throw,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def load_saving_throws(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT sp.id_salvaguarda,sl.nome_salvaguarda,sp.id_salvaguarda_personagem FROM salvaguarda_personagem sp,salvaguarda sl WHERE sp.id_personagem = %s and sl.id_salvaguarda=sp.id_salvaguarda"
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchall() 
                        if result:
                            self._saving_throws.clear()
                            for row in result:
                                self._saving_throws.append({'id_salvaguarda_personagem':row[2],'id_salvaguarda':row[0],'nome_salvaguarda':row[1]})
                            return True
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_saving_throw(self,new_id_saving_throw,last_id_saving_throw):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """UPDATE salvaguarda_personagem
                        SET id_salvaguarda=%s
                        WHERE id_salvaguarda=%s;"""
                        await mycursor.execute(query, (new_id_saving_throw,last_id_saving_throw,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def get_saving_throws(self,chave):
        await self.load_saving_throws()
        return getattr(self, f'resistencia_{chave}')
        
    @property
    def saving_throws(self):
        return {
            'forca': self.strength_resistance,
            'destreza': self.dexterity_resistance,
            'inteligencia': self.intelligence_resistance,
            'constituicao': self.constituition_resistance,
            'sabedoria': self.wisdom_resistance,
            'carisma': self.charisma_resistance,
            'salvaguardas': self.saving_throw_name_list
        }
        
    @property
    def saving_throw_name_list(self):
        lista = [d.get('nome_salvaguarda') for d in self._saving_throws]
        return lista

    @property
    def strength_resistance(self):
        if any(d.get('nome_salvaguarda') == 'forca' for d in self._saving_throws):
            return int(self.strength_bonus + self.proficiency_bonus) if self.strength_bonus is not None else int(self.proficiency_bonus)
        return int(self.strength_bonus) if self.strength_bonus is not None else None
    
    @property
    def dexterity_resistance(self):
        if any(d.get('nome_salvaguarda') == 'destreza' for d in self._saving_throws):
            return int(self.dexterity_bonus + self.proficiency_bonus) if self.dexterity_bonus is not None else int(self.proficiency_bonus)
        return int(self.dexterity_bonus) if self.dexterity_bonus is not None else None
    
    @property
    def constituition_resistance(self):
        if any(d.get('nome_salvaguarda') == 'constituicao' for d in self._saving_throws):
            return int(self.constituition_bonus + self.proficiency_bonus) if self.constituition_bonus is not None else int(self.proficiency_bonus)
        return int(self.constituition_bonus) if self.constituition_bonus is not None else None
    
    @property
    def intelligence_resistance(self):
        if any(d.get('nome_salvaguarda') == 'inteligencia' for d in self._saving_throws):
            return int(self.intelligence_bonus + self.proficiency_bonus) if self.intelligence_bonus is not None else int(self.proficiency_bonus)
        return int(self.intelligence_bonus) if self.intelligence_bonus is not None else None
    
    @property
    def wisdom_resistance(self):
        if any(d.get('nome_salvaguarda') == 'sabedoria' for d in self._saving_throws):
            return int(self.wisdom_bonus + self.proficiency_bonus) if self.wisdom_bonus is not None else int(self.proficiency_bonus)
        return int(self.wisdom_bonus) if self.wisdom_bonus is not None else None
    
    @property
    def charisma_resistance(self):
        if any(d.get('nome_salvaguarda') == 'carisma' for d in self._saving_throws):
            return int(self.charisma_bonus + self.proficiency_bonus) if self.charisma_bonus is not None else int(self.proficiency_bonus)
        return int(self.charisma_bonus) if self.charisma_bonus is not None else None