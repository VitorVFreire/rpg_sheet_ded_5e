from data import get_connection
import pymysql
import asyncio

class Equipamento:
    def __init__(self, id_equipamento = None, id_tipo_equipamento = None, nome_tipo_equipoamento = None, nome_equipamento = None, descricao = None, preco = None, peso = None, ca = None, dado = None, bonus = None):
        self.__id_tipo_equipamento = id_tipo_equipamento or []
        self.__nome_tipo_equipoamento = nome_tipo_equipoamento or []
        self.__id_equipamento = id_equipamento or []
        self.__nome_equipamento = nome_equipamento or []
        self.__descricao = descricao or []
        self.__preco = preco or []
        self.__peso = peso or []
        self.__ca = ca or []
        self.__dado = dado or []
        self.__bonus = bonus or []
        
    @property
    def equipamentos(self):
        equipamentos = []
        for id_tipo_equipamento, nome_tipo_equipamento, id_equipamento, nome_equipamento, descricao, preco, peso, ca, dado, bonus in zip(self.__id_tipo_equipamento, self.__nome_tipo_equipamento, self.__id_equipamento, self.__nome_equipamento, self.__descricao, self.__preco, self.__peso, self.__ca, self.__dado, self.__bonus):
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
                'bonus': bonus
            })
        return equipamentos
    
    @property
    def equipamento(self):
        equipamento = {
            'id_tipo_equipamento': self.__id_tipo_equipamento, 
            'nome_tipo_equipamento': self.__nome_tipo_equipamento,
            'id_equipamento': self.__id_equipamento, 
            'nome_equipamento': self.__nome_equipamento, 
            'descricao': self.__descricao,  
            'preco': self.__preco, 
            'peso': self.__peso, 
            'ca': self.__ca,
            'dado': self.__dado,
            'bonus': self.__bonus
        }
        return equipamento
   
    async def carregar_equipamentos(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT eq.id_tipo_equipamento, eq.nome_equipamento, eq.descricao, eq.preco, eq.peso, eq.ca, eq.dado, eq.bonus, eq.id_equipamento, te.nome_tipo_equipamento FROM equipamento eq, tipo_equipamento te WHERE eq.id_tipo_equipamento = te.id_tipo_equipamento;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
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
                            self.__nome_tipo_equipoamento.append(row[9])
                        return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def carregar_equipamento(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_tipo_equipamento, nome_equipamento, descricao, preco, peso, ca, dado, bonus FROM equipamento WHERE id_equipamento=%s;"
                    await mycursor.execute(query,(self._id_equipamento,))
                    result = await mycursor.fetchone() 
                    if result:
                        self.__id_tipo_equipamento = result[0]
                        self.__nome_equipamento = result[1] 
                        self.__descricao = result[2] 
                        self.__preco = result[3]
                        self.__peso = result[4]
                        self.__ca = result[5]
                        self.__dado = result[6]
                        self.__bonus = result[7]
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
                        query = "INSERT INTO equipamento (id_tipo_equipamento, nome_equipamento, descricao, preco, peso, ca, dado, bonus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
                        await mycursor.execute(query, (self.__id_tipo_equipamento, self.__nome_equipamento, self.__descricao, self.__preco, self.__peso, self.__ca, self.__dado, self.__bonus))
                        self.__id_equipamento = mycursor.lastrowid   
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False

    async def delete_equipamento_banco(self):
        try:
            if self.__id_equipamento:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from equipamento
                        WHERE id_equipamento=%s;"""
                        await mycursor.execute(query, (self.__id_equipamento,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_equipamento_banco(self, chave, valor):
        try:
            possiveis_chave = ['id_tipo_equipamento', 'nome_equipamento', 'descricao', 'preco', 'peso', 'ca', 'dado', 'bonus']
            if chave in possiveis_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE equipamento SET {chave}=%s WHERE id_equipamento=%s"""
                        await mycursor.execute(query, (valor, self._id_equipamento))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False 