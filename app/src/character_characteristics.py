from collections import OrderedDict
import asyncio
from src import Character, Image, Db

class CharacterCharacteristics(Character, Image):
    def __init__(self, user_id = None, character_id = None, parameter = None ,name = None):
        super().__init__(user_id=user_id, character_id=character_id)
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
        character_data['age'] = self.age
        character_data['height'] = self.height
        character_data['weight'] = self.weight
        character_data['eye_color'] = self.eye_color
        character_data['skin_color'] = self.skin_color
        character_data['color_hair'] = self.color_hair
        character_data['character_image'] = self.url_img

        return character_data
        
    async def exists_characteristics(self):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_characteristic_id FROM character_characteristic WHERE character_id = %s)"
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def insert_characteristics(self, key, value):
        try:
            key_possibility = ['age','eye_color','skin_color','color_hair','weight','height','character_image']
            if self.character_id and key in key_possibility:
                query = f"""INSERT INTO character_characteristic
                (character_id,{key}) 
                VALUES(%s,%s);"""
                parameters = (self.character_id, value,)
                db = Db()
                await db.connection_db()
                await db.insert(query=query, parameters=parameters)
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def delete_characteristics(self):
        try:
            if self.character_id:
                await self.load_characteristics()
                self.remove_file()
                query = """DELETE from character_characteristic
                WHERE character_id=%s;"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
    
    async def load_characteristics(self):
        try:
            if self.character_id:
                query = "SELECT age, eye_color, skin_color, color_hair, weight, height, character_image FROM character_characteristic WHERE character_id = %s"
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters, all=False)
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
        except Exception as e:
            print(e)
            return False
        
    async def update_characteristics(self,key, value):
        try:
            possibilage_key=['age','eye_color','skin_color','color_hair','weight','height','character_image']
            if self.character_id and key in possibilage_key:
                query = f"""UPDATE character_characteristic
                SET {key}=%s
                WHERE character_id=%s;"""
                parameters = (value,self.character_id)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def exists_image(self):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT id_character_characteristic FROM character_characteristic WHERE character_id = %s and character_image IS NOT NULL);"
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def save_character_image(self, file):
        try:
            exist_caracteristica = await self.exists_characteristics()
            if exist_caracteristica:
                if await self.exists_image():
                    await self.load_characteristics()
            self.parameter = self.character_id
            result, name = self.save_file(file) 
            self.set_character_image(name)
            result_final =  (
                await self.insert_characteristics(key='character_image', value=name)
                if not exist_caracteristica
                else await self.update_characteristics(key='character_image', value=name)
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