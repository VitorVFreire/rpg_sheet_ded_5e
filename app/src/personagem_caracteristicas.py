from data import get_connection
import pymysql

import asyncio

from src import Personagem, Image

class PersonagemCaracteristicas(Personagem, Image):
    def __init__(self, id_usuario = None, id_personagem = None, parametro = None ,name = None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        Image.__init__(self, parametro=parametro, name=name)
        self._caracteristicas = {
            'idade': None,
            'altura': None,
            'peso': None,
            'cor dos olhos': None,
            'cor da pele': None,
            'cor do cabelo': None
        } 
        
    async def exists_caracteristicas_banco(self):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_caracteristicas_personagem FROM caracteristicas_personagem WHERE id_personagem = %s)"
                        await mycursor.execute(query, (self.id_personagem,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def adicionar_caracteristicas_banco(self,chave, valor):
        try:
            possibilidade_chave=['idade','cor_olhos','cor_pele','cor_cabelo','peso','altura','imagem_personagem']
            if self.id_personagem and chave in possibilidade_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""INSERT INTO caracteristicas_personagem
                        (id_personagem,{chave}) 
                        VALUES(%s,%s);"""
                        await mycursor.execute(query, (self.id_personagem, valor,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_caracteristicas_banco(self):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from caracteristicas_personagem
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (self.id_personagem,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def carregar_caracteristicas_do_banco(self):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT idade, cor_olhos, cor_pele, cor_cabelo, peso, altura, imagem_personagem FROM caracteristicas_personagem WHERE id_personagem = %s"
                        await mycursor.execute(query, (self.id_personagem,))
                        result = await mycursor.fetchone() 
                        if result:
                            self.set_idade(result[0])
                            self.set_cor_olhos(result[1])
                            self.set_cor_pele(result[2])
                            self.set_cor_cabelo(result[3])
                            self.set_peso(result[4])
                            self.set_altura(result[5])
                            self.set_imagem_personagem(result[6])
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_caracteristicas_banco(self,chave, valor):
        try:
            possibilidade_chave=['idade','cor_olhos','cor_pele','cor_cabelo','peso','altura','imagem_personagem']
            if self.id_personagem and chave in possibilidade_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE caracteristicas_personagem
                        SET {chave}=%s
                        WHERE id_personagem=%s;"""
                        parametros=(valor,self.id_personagem)
                        await mycursor.execute(query, parametros)
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def exists_image_banco(self):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_caracteristicas_personagem FROM caracteristicas_personagem WHERE id_personagem = %s and imagem_personagem IS NOT NULL);"
                        await mycursor.execute(query, (self.id_personagem,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def save_img_personagem(self, file):
        try:
            exist_caracteristica = await self.exists_caracteristicas_banco()
            if exist_caracteristica:
                if await self.exists_image_banco():
                    await self.carregar_caracteristicas_do_banco()
            self.parametro = self.id_personagem
            result, name = self.save_file(file) 
            self.set_imagem_personagem(name)
            result_final =  (
                await self.adicionar_caracteristicas_banco(chave='imagem_personagem', valor=name)
                if not exist_caracteristica
                else await self.update_caracteristicas_banco(chave='imagem_personagem', valor=name)
            ) if result is True else False
            return result_final
        except Exception as e:
            print(e)
            return False
    
    @property
    def idade(self):
        return self._caracteristicas['idade'] 
        
    def set_idade(self, value):
        self._caracteristicas['idade'] = value
    
    def set_altura(self, value):
        self._caracteristicas['altura'] = value
        
    @property
    def altura(self):
        return self._caracteristicas['altura']
    
    def set_peso(self, value):
        self._caracteristicas['peso'] = value
    
    @property
    def peso(self):
        return self._caracteristicas['peso']
    
    def set_cor_olhos(self, value):
        self._caracteristicas['cor dos olhos'] = value
        
    @property
    def cor_olhos(self):
        return self._caracteristicas['cor dos olhos']
    
    def set_cor_pele(self, value):
        self._caracteristicas['cor da pele'] = value
    
    @property
    def cor_pele(self):
        return self._caracteristicas['cor da pele']
    
    def set_cor_cabelo(self, value):
        self._caracteristicas['cor do cabelo'] = value
    
    @property
    def cor_cabelo(self):
        return self._caracteristicas['cor do cabelo']  
    
    def set_imagem_personagem(self, value):
        self.name = value