from data import get_connection
import pymysql
from collections import OrderedDict
import asyncio
from src import Character, Image

class CharacterCharacteristics(Character, Image):
    def __init__(self, id_user = None, id_character = None, parameter = None ,name = None):
        super().__init__(id_user=id_user, id_character=id_character)
        Image.__init__(self, parameters=parameter, name=name)
        self._characteristics = {
            'age': None,
            'height': None,
            'weight': None,
            'eye_color': None,
            'skin_color': None,
            'color_hair': None
        } 
    
    @property
    def characteristic(self):
        character_data = OrderedDict()
        character_data['idade'] = self.age
        character_data['altura'] = self.height
        character_data['peso'] = self.weight
        character_data['cor_olhos'] = self.eye_color
        character_data['cor_pele'] = self.skin_color
        character_data['cor_cabelo'] = self.color_hair
        character_data['zimagem_personagem'] = self.url_img

        return character_data
        
    async def exists_characteristics(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_caracteristicas_personagem FROM caracteristicas_personagem WHERE id_personagem = %s)"
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def insert_characteristics(self, key, value):
        try:
            key_possibility = ['idade','cor_olhos','cor_pele','cor_cabelo','peso','altura','imagem_personagem']
            if self.id_character and key in key_possibility:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""INSERT INTO caracteristicas_personagem
                        (id_personagem,{key}) 
                        VALUES(%s,%s);"""
                        await mycursor.execute(query, (self.id_character, value,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_characteristics(self):
        try:
            if self.id_character:
                await self.load_characteristics()
                self.remove_file()
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from caracteristicas_personagem
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (self.id_character,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def load_characteristics(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT idade, cor_olhos, cor_pele, cor_cabelo, peso, altura, imagem_personagem FROM caracteristicas_personagem WHERE id_personagem = %s"
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchone() 
                        if result:
                            self.set_age(result[0])
                            self.set_eye_color(result[1])
                            self.set_skin_color(result[2])
                            self.set_color_hair(result[3])
                            self.set_weight(result[4])
                            self.set_height(result[5])
                            self.set_character_image(result[6])
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_characteristics(self,chave, valor):
        try:
            possibilidade_chave=['idade','cor_olhos','cor_pele','cor_cabelo','peso','altura','imagem_personagem']
            if self.id_character and chave in possibilidade_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE caracteristicas_personagem
                        SET {chave}=%s
                        WHERE id_personagem=%s;"""
                        parametros=(valor,self.id_character)
                        await mycursor.execute(query, parametros)
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def exists_image(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_caracteristicas_personagem FROM caracteristicas_personagem WHERE id_personagem = %s and imagem_personagem IS NOT NULL);"
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def save_character_image(self, file):
        try:
            exist_caracteristica = await self.exists_characteristics()
            if exist_caracteristica:
                if await self.exists_image():
                    await self.load_characteristics()
            self.parameter = self.id_character
            result, name = self.save_file(file) 
            self.set_character_image(name)
            result_final =  (
                await self.insert_characteristics(key='imagem_personagem', value=name)
                if not exist_caracteristica
                else await self.update_characteristics(chave='imagem_personagem', valor=name)
            ) if result is True else False
            return result_final
        except Exception as e:
            print(e)
            return False
    
    @property
    def age(self):
        return self._characteristics['age'] 
        
    def set_age(self, value):
        self._characteristics['age'] = value
    
    def set_height(self, value):
        self._characteristics['height'] = value
        
    @property
    def height(self):
        return self._characteristics['height']
    
    def set_weight(self, value):
        self._characteristics['weight'] = value
    
    @property
    def weight(self):
        return self._characteristics['weight']
    
    def set_eye_color(self, value):
        self._characteristics['eye_color'] = value
        
    @property
    def eye_color(self):
        return self._characteristics['eye_color']
    
    def set_skin_color(self, value):
        self._characteristics['skin_color'] = value
    
    @property
    def skin_color(self):
        return self._characteristics['skin_color']
    
    def set_color_hair(self, value):
        self._characteristics['color_hair'] = value
    
    @property
    def color_hair(self):
        return self._characteristics['color_hair']  
    
    def set_character_image(self, value):
        self.name = value