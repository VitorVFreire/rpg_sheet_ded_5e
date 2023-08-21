from data import get_connection
from src import Usuario
import pymysql
import asyncio

from src import Personagem

class PersonagemHabilidades(Personagem):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        self._feitico = []
        
    async def adicionar_feitico_banco(self,id_feitico):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO feitico_personagem(id_personagem,id_feitico) VALUES(%s,%s);"
                        await mycursor.execute(query, (self._id_personagem,id_feitico))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_feitico_banco(self,id_feitico_personagem):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from feitico_personagem
                        WHERE id_feitico_personagem=%s;"""
                        await mycursor.execute(query, (id_feitico_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def carregar_feiticos_do_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT fp.id_feitico, ft.nome_feitico, ft.tipo_feitico, td.nome_tipo,fp.id_feitico_personagem
                        FROM feitico_personagem fp
                        JOIN feitico ft ON fp.id_feitico = ft.id_feitico
                        JOIN tipo_dano td ON ft.id_tipo_dano = td.id_tipo_dano
                        WHERE fp.id_personagem = %s;"""
                        await mycursor.execute(query, (self._id_personagem))
                        result = await mycursor.fetchall()
                        if result:
                            for row in result:
                                feitico = {
                                    'id_feitico_personagem':row[4],
                                    'id_feitico': row[0],
                                    'nome_feitico': row[1],
                                    'tipo_feitico': row[2],
                                    'tipo_dano':row[3]
                                }
                                self.feitico(feitico)               
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_feitico_banco(self,novo_feitico,id_feitico_personagem):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """UPDATE feitico_personagem
                        SET id_feitico=%s
                        WHERE id_feitico_personagem=%s;"""
                        await mycursor.execute(query, (novo_feitico,id_feitico_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    def feitico(self,value):
        return self._feitico[value]
    
    @property
    def feiticos(self):
        return self._feitico  
    
    @feitico.setter
    def feitico(self,value):
        self._feitico.append(value)