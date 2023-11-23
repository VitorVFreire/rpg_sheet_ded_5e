from src import User, Db, Moeda
import asyncio
from flask import abort
import datetime

class Character(User, Moeda):
    def __init__(self, user_id=None, character_id=None, value=None):
        super().__init__(user_id=user_id)
        Moeda().__init__(self, value=value)
        self._character_id = character_id
        self._character_name = None
        self._classes = []
        self._race = None
    
    @property
    def character_id(self):
        return self._character_id 
    
    @property
    def classe(self):
        return self._classes[0]['class_name'] if len(self._classes) > 0 else ''
    
    @property
    def classes(self):
        return self._classes

    @classe.setter
    def classe(self, value):
        self._classes.append(value)
        
    @property
    def character_name(self):
        return self._character_name
        
    @character_name.setter
    def character_name(self,value):
        self._character_name=value 
        
    @property
    def race(self):
        return self._race
    
    @race.setter
    def race(self,value):
        self._race=value   
        
    @property
    def character(self):
        character = {
            'character_id': self.character_id,
            'character_name': self.character_name,
            'race': self.race,
            'classes': self.classes
        }
        return character
        
    async def character_belongs_user(self):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_id FROM character WHERE character_id = %s and user_id = %s)"
                parameters = (self.character_id, self.user_id)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            abort(403, "Acesso Negado")
        except Exception as e:
            print(e)
            return False      

    async def insert_character_class(self,class_id):
        try:
            if self.character_id:
                query = """
                    INSERT INTO character_class 
                    (character_id, class_id)
                    VALUES (%s, %s);
                """
                parameters = (self.character_id, class_id)
                db = Db()
                await db.connection_db()
                await db.insert(query=query, parameters=parameters)
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def delete_character_class(self,character_class_id):
        try:
            if self.character_id:
                query = """DELETE from character_class
                WHERE character_class_id=%s;"""
                parameters = (character_class_id,)
                db = Db()
                await db.connection_db()
                return db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
    
    async def insert_character(self,race_id,character_name):
        try:
            if self.user_id:
                query = """INSERT INTO character
                (user_id,race_id,character_name, date_creation) 
                VALUES(%s,%s,%s,%s)
                RETURNING character_id;"""
                parameters = (self.user_id, race_id, character_name, datetime.date.today())
                db = Db()
                await db.connection_db()
                self._character_id = await db.insert(query=query, parameters=parameters) 
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def delete_character(self):
        try:
            if self.character_id:
                query = """DELETE from character
                WHERE character_id=%s;"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def update_character_class(self,class_id,character_class_id):
        try:
            if self.character_id:
                query = """UPDATE classe_character
                SET class_id=%s
                WHERE character_class_id=%s"""
                parameters = (class_id,character_class_id,)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_character_classes(self):
        try:
            if self.character_id:
                query = """SELECT cp.class_id, cl.class_name, cp.character_class_id
                FROM character_class cp, class cl
                WHERE cp.character_id = %s and cp.class_id=cl.class_id;"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    self._classes.clear()
                    for row in result:
                        self._classes.append({'character_class_id': row[2], 'class_id': row[0], 'class_name': row[1]})
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_character(self):
        try:
            if self.character_id:
                query = """SELECT ch.character_name,rc.race_name
                FROM character ch,race rc
                WHERE ch.character_id = %s and ch.race_id=rc.race_id;"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters, all=False)
                if result:
                    self.character_name=result[0]
                    self.race=result[1]
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def update_character(self,key,value):
        try:
            possibilidades_key=['race_id','character_name']
            if self.character_id and key in possibilidades_key:
                query = f"""UPDATE character
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
     
"""    async def exists_moeda_banco(self, moeda):
        try:
            if self._character_id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_moedas_character FROM moeda WHERE character_id = %s AND moeda = %s)"
                        await mycursor.execute(query, (self._character_id, moeda,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except Exception as e:
            print(e)
            return False    
        
    async def banco_moeda_character(self, moeda):
        try:
            if self._character_id and self.verifica_moeda(moeda):
                async with await get_connection() as conn:
                        async with conn.cursor() as mycursor:
                            if await self.exists_moeda_banco(moeda):
                                query = f"UPDATE moedas_character SET qtd=%s WHERE character_id=%s AND moeda=%s;"
                                parametros = (self.value, self.character_id, moeda,)
                            else:
                                query = f"INSERT INTO moedas_character(character_id,moeda,qtd) VALUES(%s,%s,%s);"
                                parametros = (self._character_id, moeda, self.value)
                            await mycursor.execute(query, parametros)
                            await conn.commit()
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def gasto_moeda(self):
        try:
            if self._character_id:
                async with await get_connection() as conn:
                        async with conn.cursor() as mycursor:
                            deposito, saque = self.converter_moedas()
                            if self.exists_moeda_banco(self.destino):
                                query = "UPDATE moedas_character SET qtd=%s WHERE moeda=%s AND character_id=%s;"
                            else:
                                query = "INSERT INTO moedas_character (qtd_moeda, moeda, character_id) VALUES(%s,%s,%s);"                            
                            query += "UPDATE moedas_character SET qtd=%s WHERE character_id=%s AND moeda=%s;"
                            parametros = (deposito, self.destino, self.character_id, saque, self.character_id, self.origem,)
                            await mycursor.execute(query, parametros)
                            await conn.commit()
                            return True
            return False
        except Exception as e:
            print(e)
            return False"""