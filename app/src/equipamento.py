from data import get_connection
import pymysql
import asyncio
from flask import url_for

from src import Image

class Equipamento(Image):
    def __init__(self, id_equipamento = None, id_tipo_equipamento = None, nome_tipo_equipamento = None, nome_equipamento = None, descricao = None, preco = None, peso = None, ca = None, dado = None, bonus = None, name = None, imagem_equipamento = None):
        super().__init__(parametro=id_equipamento,name=name)
        self.__id_tipo_equipamento = [id_tipo_equipamento]
        self.__nome_tipo_equipamento = [nome_tipo_equipamento]
        self.__id_equipamento = [id_equipamento]
        self.__nome_equipamento = [nome_equipamento]
        self.__descricao = [descricao]
        self.__preco = [preco]
        self.__peso = [peso]
        self.__ca = [ca]
        self.__dado = [dado]
        self.__bonus = [bonus]
        self.__imagem_equipamento = [imagem_equipamento]
        self.__equiapamentos_personagem = []
    
    @property
    def imagem_equipamentos(self):
        return self.__imagem_equipamento
            
    @imagem_equipamentos.setter
    def imagem_equipamentos(self, value):
        self.name = value
        self.__imagem_equipamento.append(self.url_img)
        
    @property
    def equipamentos(self):
        equipamentos = []
        for id_tipo_equipamento, nome_tipo_equipamento, id_equipamento, nome_equipamento, descricao, preco, peso, ca, dado, bonus, imagem_equipamento in zip(self.__id_tipo_equipamento, self.__nome_tipo_equipamento, self.__id_equipamento, self.__nome_equipamento, self.__descricao, self.__preco, self.__peso, self.__ca, self.__dado, self.__bonus, self.imagem_equipamentos):
            equipamentos.append({
                'id_tipo_equipamento': id_tipo_equipamento, 
                'nome_tipo_equipamento': nome_tipo_equipamento,
                'id_equipamento': id_equipamento, 
                'nome_equipamento': nome_equipamento, 
                'descricao': descricao,  
                'preco': preco, 
                'peso': peso, 
                'ca': ca,
                'dado': dado,
                'bonus': bonus,
                'imagem_equipamento': imagem_equipamento,
                'personagem_possui': id_equipamento in self.__equiapamentos_personagem
            })
        return equipamentos if equipamentos[0]['id_equipamento'] is not None else None
    
    @property
    def equipamento(self):
        equipamento = {
            'id_tipo_equipamento': self.id_tipo_equipamento, 
            'nome_tipo_equipamento': self.__nome_tipo_equipamento,
            'id_equipamento': self.id_equipamento, 
            'nome_equipamento': self.nome_equipamento, 
            'descricao': self.descricao,  
            'preco': self.preco, 
            'peso': self.peso, 
            'ca': self.ca,
            'dado': self.dado,
            'bonus': self.bonus,
            'imagem_equipamento': self.imagem_equipamento,
            'personagem_possui': self.__id_equipamento in self.__equiapamentos_personagem
        }
        return equipamento if equipamento['id_equipamento'] is not None else None
    
    def clear_equipamentos(self):
        if self.__id_equipamento[0] is None:
            self.__id_tipo_equipamento.clear()
            self.__nome_tipo_equipamento.clear()
            self.__id_equipamento.clear()
            self.__nome_equipamento.clear()
            self.__descricao.clear()
            self.__preco.clear()
            self.__peso.clear()
            self.__ca.clear()
            self.__dado.clear()
            self.__bonus.clear()
            self.__imagem_equipamento.clear()

    @property
    def tipo_equipamentos(self):
        tipo_equipamento = []
        for id_tipo_equipamento, nome_tipo_equipamento in zip(self.__id_tipo_equipamento, self.__nome_tipo_equipamento):
            tipo_equipamento.append({
                'id_tipo_equipamento': id_tipo_equipamento, 
                'nome_tipo_equipamento': nome_tipo_equipamento
            })
        return tipo_equipamento
    
    async def carregar_tipo_equipamentos(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_tipo_equipamento, nome_tipo_equipamento FROM tipo_equipamento;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        self.clear_equipamentos()
                        for row in result:
                            self.__id_tipo_equipamento.append(row[0])
                            self.__nome_tipo_equipamento.append(row[1])
                        return True
            return False
        except Exception as e:
            print(e)
            return False

    async def carregar_equiapamentos_personagem_do_banco(self, id_personagem):
        try:
            if id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT id_equipamento FROM equipamento_personagem WHERE id_personagem = %s;"""
                        await mycursor.execute(query, (id_personagem,))
                        result = await mycursor.fetchall()
                        if result:
                            for row in result:
                                self.__equiapamentos_personagem.append(row[0])              
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
   
    async def carregar_equipamentos(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT eq.id_tipo_equipamento, eq.nome_equipamento, eq.descricao, eq.preco, eq.peso, eq.ca, eq.dado, eq.bonus, eq.id_equipamento, te.nome_tipo_equipamento, eq.imagem_equipamento FROM equipamento eq, tipo_equipamento te WHERE eq.id_tipo_equipamento = te.id_tipo_equipamento;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        self.clear_equipamentos()
                        for row in result:
                            self.__id_tipo_equipamento.append(row[0])
                            self.__nome_equipamento.append(row[1]) 
                            self.__descricao.append(row[2]) 
                            self.__preco.append(row[3])
                            self.__peso.append(row[4])
                            self.__ca.append(row[5])
                            self.__dado.append(row[6])
                            self.__bonus.append(row[7])
                            self.__id_equipamento.append(row[8])
                            self.__nome_tipo_equipamento.append(row[9])
                            self.imagem_equipamentos = row[10]
                        return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def carregar_equipamento(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_tipo_equipamento, nome_equipamento, descricao, preco, peso, ca, dado, bonus, imagem_equipamento FROM equipamento WHERE id_equipamento=%s;"
                    await mycursor.execute(query,(self.id_equipamento,))
                    result = await mycursor.fetchone() 
                    if result:
                        self.clear_equipamentos()
                        self.__id_tipo_equipamento.append(result[0])
                        self.__nome_equipamento.append(result[1]) 
                        self.__descricao.append(result[2]) 
                        self.__preco.append(result[3])
                        self.__peso.append(result[4])
                        self.__ca.append(result[5])
                        self.__dado.append(result[6])
                        self.__bonus.append(result[7])
                        self.imagem_equipamentos(result[8])
                        return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_equipamento_banco(self):
        try:
            if self.__id_tipo_equipamento:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        self.__imagem_equipamento[0] = self.save_img_equipamento(self.imagem_equipamento) if self.imagem_equipamento is not None else None
                        query = "INSERT INTO equipamento (id_tipo_equipamento, nome_equipamento, descricao, preco, peso, ca, dado, bonus, imagem_equipamento) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                        await mycursor.execute(query, (self.id_tipo_equipamento, self.nome_equipamento, self.descricao, self.preco, self.peso, self.ca, self.dado, self.bonus, self.imagem_equipamento))
                        self.__id_equipamento[0] = mycursor.lastrowid   
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            self.name = self.imagem_equipamento
            self.remove_file()
            print(e)
            return False

    async def delete_equipamento_banco(self):
        try:
            if self.__id_equipamento:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from equipamento
                        WHERE id_equipamento=%s;"""
                        await mycursor.execute(query, (self.id_equipamento,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_equipamento_banco(self, chave, valor):
        try:
            possiveis_chave = ['id_tipo_equipamento', 'nome_equipamento', 'descricao', 'preco', 'peso', 'ca', 'dado', 'bonus', 'imagem_equipamento']
            if chave in possiveis_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE equipamento SET {chave}=%s WHERE id_equipamento=%s"""
                        await mycursor.execute(query, (valor, self.id_equipamento))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False 
    
    def save_img_equipamento(self, file):
        try:
            self.parametro = 'equipamento'
            result, name = self.save_file(file) 
            return name if result is True else None
        except Exception as e:
            print(e)
            return False       
        
    @property
    def ca(self):
        if isinstance(self.__ca, list) and self.__ca[0] == '':
            return None
        return self.__ca[0]
    
    @property
    def id_equipamento(self):
        if isinstance(self.__id_equipamento, list) and self.__id_equipamento[0] == '':
            return None
        return self.__id_equipamento[0]
    
    @property
    def id_tipo_equipamento(self):
        if isinstance(self.__id_tipo_equipamento, list) and self.__id_tipo_equipamento[0] == '':
            return None
        return self.__id_tipo_equipamento[0]
    
    @property
    def nome_tipo_equipamento(self):
        if isinstance(self.__nome_tipo_equipamento, list) and self.__nome_tipo_equipamento[0] == '':
            return None
        return self.__nome_tipo_equipamento[0]
    
    @property
    def nome_equipamento(self):
        if isinstance(self.__nome_equipamento, list) and self.__nome_equipamento[0] == '':
            return None
        return self.__nome_equipamento[0]
    
    @property
    def descricao(self):
        if isinstance(self.__descricao, list) and self.__descricao[0] == '':
            return None
        return self.__descricao[0]
    
    @property
    def imagem_equipamento(self):
        if isinstance(self.__imagem_equipamento, list) and self.__imagem_equipamento[0] == '':
            return None
        return self.__imagem_equipamento[0]
    
    @property
    def preco(self):
        if isinstance(self.__preco, list) and self.__preco[0] == '':
            return None
        return self.__preco[0]
    
    @property
    def peso(self):
        if isinstance(self.__peso, list) and self.__peso[0] == '':
            return None
        return self.__peso[0]
    
    @property
    def dado(self):
        if isinstance(self.__dado, list) and self.__dado[0] == '':
            return None
        return self.__dado[0]
    
    @property
    def bonus(self):
        if isinstance(self.__bonus, list) and self.__bonus[0] == '':
            return None
        return self.__bonus[0]
    