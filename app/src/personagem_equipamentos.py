from data import get_connection
import pymysql
import asyncio

from src import Personagem

class PersonagemEquipamento(Personagem):
    def __init__(self, id_usuario=None,id_personagem=None, id_equipamento = None, qtd = None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        self.__id_equipamento = id_equipamento
        self.__qtd = qtd
        self._equipamento = []
    
    async def exists_equipamento_especifica_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_equipamento_personagem FROM equipamento_personagem WHERE id_equipamento = %s and id_personagem = %s)"
                        await mycursor.execute(query, (self.__id_equipamento,self._id_personagem,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def exists_equipamento_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_equipamento_personagem FROM equipamento_personagem WHERE id_personagem = %s)"
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def adicionar_equipamento_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO equipamento_personagem(id_equipamento, id_personagem, qtd) VALUES(%s,%s,%s);"
                        await mycursor.execute(query, (self.__id_equipamento, self._id_personagem, self.__qtd))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_equipamento_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from equipamento_personagem
                        WHERE id_equipamento=%s and id_personagem = %s;"""
                        await mycursor.execute(query, (self.__id_equipamento_personagem, self._id_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def carregar_equipamentos_do_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT eq.id_tipo_equipamento, eq.nome_equipamento, eq.descricao, eq.preco, eq.peso, eq.ca, eq.dado, eq.bonus, eq.id_equipamento, te.nome_tipo_equipamento, ep.id_equipamento_personagem, ep.qtd
                        FROM equipamento eq, tipo_equipamento te, equipamento_personagem ep 
                        WHERE eq.id_tipo_equipamento = te.id_tipo_equipamento AND ep.id_equipamento = eq.id_equipamento AND ep.id_personagem = %s;"""
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchall() 
                        if result:
                            for row in result:
                                self.equipamento({
                                    'id_tipo_equipamento': row[0],
                                    'nome_equipamento': row[1], 
                                    'descricao': row[2], 
                                    'preco': row[3],
                                    'peso': row[4],
                                    'ca': row[5],
                                    'dado': row[6],
                                    'bonus': row[7],
                                    'id_equipamento': row[8],
                                    'nome_tipo_equipoamento': row[9],
                                    'id_equipamento_personagem': row[10],
                                    'qtd': row[11]
                                })
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_equipamento_banco(self, id_equipamento_personagem, chave):
        try:
            possibilidade_chave = ['id_equipamento', 'qtd']
            if self._id_personagem and chave in possibilidade_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        valor = getattr(self, f"__{chave}")
                        query = f"""UPDATE equipamento_personagem
                        SET {chave}=%s
                        WHERE id_equipamento_personagem=%s;"""
                        await mycursor.execute(query, (valor, id_equipamento_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    def equipamento(self, value):
        return self._equipamento[value]
    
    @property
    def equipamentos(self):
        return self._equipamento  
    
    @equipamento.setter
    def equipamento(self, value):
        self._equipamento.append(value)