from data import get_connection
from src import Usuario
import pymysql
import asyncio
from flask import abort

class Personagem(Usuario):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id=id_usuario)
        self._id_personagem = id_personagem
        self._nome_personagem=None
        self._classe = []
        self._raca = None
        self._armas=[]
        self._equipamentos=[]      
        
    async def personagem_pertence_usuario(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_personagem FROM personagem WHERE id_personagem = %s and id_usuario = %s)"
                        await mycursor.execute(query, (self._id_personagem, self.id))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            abort(403, "Acesso Negado")
        except pymysql.Error as e:
            print(e)
            return False      
        
    @property
    def id_personagem(self):
        return self._id_personagem

    async def adicionar_classe_banco(self,id_classe):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """
                            INSERT INTO `RPG`.`classe_personagem` 
                            (`id_personagem`, `id_classe`)
                            VALUES (%s, %s)
                        """
                        await mycursor.execute(query, (self._id_personagem,id_classe))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_classe_banco(self,id_classe_personagem):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from classe_personagem
                        WHERE id_classe_personagem=%s;"""
                        await mycursor.execute(query, (id_classe_personagem,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def adicionar_personagem_banco(self,id_raca,nome_personagem):
        try:
            if self._id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """INSERT INTO personagem
                        (id_usuario,id_raca,nome_personagem) 
                        VALUES(%s,%s,%s);"""
                        await mycursor.execute(query, (self._id,id_raca,nome_personagem))
                        self._id_personagem = mycursor.lastrowid  
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def delete_personagem_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from personagem
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (self._id_personagem,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_classe_banco(self,id_classe,id_classe_personagem):
        try:
            if self._id_personagem:
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
        
    async def carregar_classe_do_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT cp.id_classe, cl.nome_classe,cp.id_classe_personagem
                        FROM classe_personagem cp, classe cl
                        WHERE cp.id_personagem = %s and cp.id_classe=cl.id_classe;"""
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchall()
                        if result:
                            await self._classe.clear()
                            for row in result:
                                self._classe.append({'id_classe_personagem': row[2], 'id_classe': row[0], 'nome_classe': row[1]})
                                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    async def classe(self):
        if len(self._classe)<=0:
            await self.carregar_classe_do_banco()
        return self._classe

    @classe.setter
    def classe(self, value):
        self._classe.append(value)
        
    async def carregar_personagem_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT pr.nome_personagem,rc.nome_raca
                        FROM personagem pr,raca rc
                        WHERE pr.id_personagem = %s and pr.id_raca=rc.id_raca;"""
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchone()
                        if result:
                            self.nome_personagem=result[0]
                            self.raca=result[1]
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    async def nome_personagem(self):
        if self._nome_personagem is None:
            await self.carregar_personagem_banco()
        return self._nome_personagem
        
    @nome_personagem.setter
    def nome_personagem(self,value):
        self._nome_personagem=value
        
    async def update_personagem_banco(self,chave,valor):
        try:
            possibilidades_chave=['id_raca','nome_personagem']
            if self._id_personagem and chave in possibilidades_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE personagem
                        SET {chave}=%s
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (valor,self._id_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    async def raca(self):
        if self._raca is None:
            await self.carregar_personagem_banco()
        return self._raca
    
    @raca.setter
    def raca(self,value):
        self._raca=value