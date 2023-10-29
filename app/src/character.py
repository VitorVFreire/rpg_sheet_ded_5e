from data import get_connection
from src import User, Moeda
import pymysql
import asyncio
from flask import abort

class Character(User, Moeda):
    def __init__(self, id_user=None, id_character=None, value=None):
        super().__init__(id_user=id_user)
        Moeda().__init__(self, valor=value)
        self._id_character = id_character
        self._character_name = None
        self._classes = []
        self._race = None
    
    @property
    def id_character(self):
        return self._id_character 
    
    @property
    def classe(self):
        return self._classes[0]['nome_classe'] if len(self._classes) > 0 else ''
    
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
        
    async def character_belongs_user(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_personagem FROM personagem WHERE id_personagem = %s and id_usuario = %s)"
                        await mycursor.execute(query, (self.id_character, self.id_user))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            abort(403, "Acesso Negado")
        except pymysql.Error as e:
            print(e)
            return False      

    async def insert_character_class(self,id_class):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """
                            INSERT INTO `RPG`.`classe_personagem` 
                            (`id_personagem`, `id_classe`)
                            VALUES (%s, %s)
                        """
                        await mycursor.execute(query, (self.id_character,id_class))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_character_class(self,id_character_class):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from classe_personagem
                        WHERE id_classe_personagem=%s;"""
                        await mycursor.execute(query, (id_character_class,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def insert_character(self,id_race,character_name):
        try:
            if self.id_user:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """INSERT INTO personagem
                        (id_usuario,id_raca,nome_personagem) 
                        VALUES(%s,%s,%s);"""
                        await mycursor.execute(query, (self.id_user,id_race,character_name))
                        self._id_character = mycursor.lastrowid  
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def delete_character(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from personagem
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (self.id_character,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_character_class(self,id_classe,id_classe_personagem):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """UPDATE classe_personagem
                        SET id_classe=%s
                        WHERE id_classe_personagem=%s"""
                        await mycursor.execute(query, (id_classe,id_classe_personagem,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def load_character_classes(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT cp.id_classe, cl.nome_classe,cp.id_classe_personagem
                        FROM classe_personagem cp, classe cl
                        WHERE cp.id_personagem = %s and cp.id_classe=cl.id_classe;"""
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchall()
                        if result:
                            self._classes.clear()
                            for row in result:
                                self._classes.append({'id_classe_personagem': row[2], 'id_classe': row[0], 'nome_classe': row[1]})
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def load_character(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT pr.nome_personagem,rc.nome_raca
                        FROM personagem pr,raca rc
                        WHERE pr.id_personagem = %s and pr.id_raca=rc.id_raca;"""
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchone()
                        if result:
                            self.character_name=result[0]
                            self.race=result[1]
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_character(self,chave,valor):
        try:
            possibilidades_chave=['id_raca','nome_personagem']
            if self.id_character and chave in possibilidades_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE personagem
                        SET {chave}=%s
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (valor,self.id_character))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
     
"""    async def exists_moeda_banco(self, moeda):
        try:
            if self._id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_moedas_personagem FROM moeda WHERE id_personagem = %s AND moeda = %s)"
                        await mycursor.execute(query, (self._id_character, moeda,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False    
        
    async def banco_moeda_personagem(self, moeda):
        try:
            if self._id_character and self.verifica_moeda(moeda):
                async with await get_connection() as conn:
                        async with conn.cursor() as mycursor:
                            if await self.exists_moeda_banco(moeda):
                                query = f"UPDATE moedas_personagem SET qtd=%s WHERE id_personagem=%s AND moeda=%s;"
                                parametros = (self.valor, self.id_character, moeda,)
                            else:
                                query = f"INSERT INTO moedas_personagem(id_personagem,moeda,qtd) VALUES(%s,%s,%s);"
                                parametros = (self._id_character, moeda, self.valor)
                            await mycursor.execute(query, parametros)
                            await conn.commit()
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def gasto_moeda(self):
        try:
            if self._id_character:
                async with await get_connection() as conn:
                        async with conn.cursor() as mycursor:
                            deposito, saque = self.converter_moedas()
                            if self.exists_moeda_banco(self.destino):
                                query = "UPDATE moedas_personagem SET qtd=%s WHERE moeda=%s AND id_personagem=%s;"
                            else:
                                query = "INSERT INTO moedas_personagem (qtd_moeda, moeda, id_personagem) VALUES(%s,%s,%s);"                            
                            query += "UPDATE moedas_personagem SET qtd=%s WHERE id_personagem=%s AND moeda=%s;"
                            parametros = (deposito, self.destino, self.id_character, saque, self.id_character, self.origem,)
                            await mycursor.execute(query, parametros)
                            await conn.commit()
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False"""