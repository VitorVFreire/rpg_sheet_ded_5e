from data import get_connection
from src import Usuario
import pymysql
import asyncio

from src import Personagem

class PersonagemHabilidades(Personagem):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        self._habilidade = []
    
    async def exists_habilidade_banco(self, id_habilidade):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_habilidade_personagem FROM habilidade_personagem WHERE id_habilidade = %s and id_personagem = %s)"
                        await mycursor.execute(query, (id_habilidade,self._id_personagem,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def adicionar_habilidade_banco(self,id_habilidade):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO habilidade_personagem(id_personagem,id_habilidade) VALUES(%s,%s);"
                        await mycursor.execute(query, (self._id_personagem,id_habilidade))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_habilidade_banco(self,id_habilidade_personagem):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from habilidade_personagem
                        WHERE id_habilidade=%s and id_personagem = %s;"""
                        await mycursor.execute(query, (id_habilidade_personagem, self._id_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def carregar_habilidades_do_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT hb.id_habilidade, hb.nome_habilidade, hb.nome_atributo, hb.nivel_habilidade, hb.tipo_dano, hb.qtd_dados, hb.lados_dados, hb.adicional_por_nivel, hb.link_detalhes, hp.id_habilidade_personagem
                        FROM habilidade_personagem hp
                        JOIN habilidade hb ON hp.id_habilidade = hb.id_habilidade
                        WHERE hp.id_personagem = %s;"""
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchall()
                        if result:
                            for row in result:
                                habilidade = {
                                    'id_habilidade': row[0],
                                    'nome_habilidade': row[1],
                                    'nome_atributo': row[2],
                                    'nivel_habilidade': row[3],
                                    'tipo_dano': row[4],
                                    'qtd_dados': row[5],
                                    'lados_dados': row[6],
                                    'adicional_por_nivel': row[7],
                                    'link_detalhes': row[8],
                                    'id_habilidade_personagem': row[9]
                                }
                                self.habilidade = habilidade              
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_habilidade_banco(self,novo_habilidade,id_habilidade_personagem):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """UPDATE habilidade_personagem
                        SET id_habilidade=%s
                        WHERE id_habilidade_personagem=%s;"""
                        await mycursor.execute(query, (novo_habilidade,id_habilidade_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    def habilidade(self, value):
        return self._habilidade[value]
    
    @property
    def habilidades(self):
        return self._habilidade  
    
    @habilidade.setter
    def habilidade(self,value):
        self._habilidade.append(value)