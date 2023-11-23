import datetime
import asyncio
import base64
from hashlib import sha256

from src import Image, Db

class User:
    def __init__(self, user_id=None, user_name=None, email=None, password=None, birth_date=None):
        self.__user_id = user_id
        self._user_name = user_name
        self._email = email
        self.__password = self.encrypt(password)
        self.__user_type = None
        self._birth_date  =  birth_date
        self._characters = []
        
    @property
    def user_type(self):
        return self.__user_type   
    
    async def valid_admin_user(self):
        await self.load_user()
        return self.user_type == 1  
    
    @property
    def characters(self):
        return self._characters
    
    @property
    def user_id(self):
        return self.__user_id
    
    @user_id.setter
    def user_id(self,value):
        self.__user_id = value
    
    @property
    def user_name(self): 
        return self._user_name
    
    @user_name.setter
    def user_name(self,value):
        self._user_name = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value
    
    @property
    def age(self):
        today = datetime.date.today()
        birth_date_str = self._birth_date.strftime('%Y-%m-%d')
        dif = today - datetime.datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        return dif.days // 365 if dif.days is not None else None
    
    @age.setter
    def age(self, value):
        self._birth_date = value
        
    def encrypt(self, value):
        if value is None:
            return None
        hash_password = sha256(value.encode())
        password_digest = hash_password.digest()
        return base64.b64encode(password_digest).decode('utf-8')
            
    async def delete_user(self):
        try:
            db = Db()
            await db.connection_db()
            if self.user_id:
                return await db.delete('DELETE from "user" WHERE user_id=%s;', (self.user_id,))
            elif self._email:
                return await db.delete('DELETE from "user" WHERE email=%s;', (self._email,))
            return False
        except Exception as e:
            print(e)
            return False   
    
    async def insert_user(self):
        try:
            if self._user_name and self._email and self.__password and self._birth_date:
                db = Db()
                await db.connection_db()
                query = 'INSERT INTO "user"(user_name, password, email, birth_date, date_creation) VALUES(%s, %s, %s, %s, %s) RETURNING user_id;'
                parameters = (self.user_name, self.__password, self.email, self._birth_date, datetime.date.today())
                self.user_id = await db.insert(query=query, parameters=parameters)
                return True
        except Exception as e:
                print(e)
                return False
        return False
    
    async def update_user(self, key, value):
        try:
            possiveis_key=['user_name','email','password','birth_date','user_type']
            if self.user_id and key in possiveis_key:
                if key == 'password':
                    value = self.encrypt(value)
                db = Db()
                await db.connection_db()
                query = f"UPDATE usuario SET {key} = %s WHERE user_id = %s;"
                parameters = (value, self.user_id)
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_user(self):
        try:
            if self.user_id:
                query = 'SELECT user_id, user_name, email, password, birth_date, user_type FROM "user" WHERE user_id=%s'
                parameters = (self.user_id,)
            elif self._email:
                query = 'SELECT user_id, user_name, email, password, birth_date, user_type FROM "user" WHERE email=%s'
                parameters = (self._email,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self.user_id = result[0]
                self.user_name = result[1]
                self.email = result[2]
                self.password = result[3]
                self.age = result[4]
                self.__user_type = result[5]
                return True
            return None
        except Exception as e:
            print(e)
            return False
    
    async def user_validate(self):            
        try:
            if self._email and self.__password:
                query = 'SELECT user_id, user_name, user_type, birth_date FROM "user" WHERE email=%s and password=%s'
                parameters = (self._email,self.__password,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters, all=False)
                if result:
                    self.user_id=result[0]
                    self._user_name=result[1]
                    self.__user_type=result[2]
                    self._birth_date=result[3]
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_characters(self):
        try:
            if self.user_id:
                query = """SELECT ch.character_id, ch.character_name, rc.race_name, rc.race_id, COALESCE(cc.character_image, null) AS character_image
                FROM character ch
                LEFT JOIN character_characteristic cc ON cc.character_id = ch.character_id
                JOIN race rc ON ch.race_id = rc.race_id
                WHERE ch.user_id = %s;"""
                parameters = (self.user_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    image = Image()
                    for row in result:
                        image.user_name = row[4]
                        self._characters.append({'character_id':row[0],'character_name':row[1],'race_name':row[2],'race_id':row[3],'img': image.url_img})
                    return True
            return 'Sem Personagens no Banco', False
        except Exception as e:
            print(e)
            return False 