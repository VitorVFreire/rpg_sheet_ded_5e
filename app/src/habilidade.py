from data import get_connection
import pymysql
import asyncio

class Habilidade:
    def __init__(self, id_habilidade=None, nome_habilidade=None, tipo_dano = None, dado_habilidade = None, nivel_habilidade = None, adicional_por_nivel = None):
        self._id_habilidade = id_habilidade or []
        self._nome_habilidade = nome_habilidade or []
        self._dado_habilidade = dado_habilidade or []
        self._adicional_por_nivel = adicional_por_nivel or [] 
        self._tipo_dano = tipo_dano or []
        self._nivel_habilidade = nivel_habilidade or []
   
    async def carregar_habilidades(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_habilidade, nome_habilidade, nivel_habilidade, dado_habilidade, adicional_por_nivel, tipo_dano FROM habilidade;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        for row in result:
                            self._id_habilidade.append(row[0])
                            self._nome_habilidade.append(row[1])
                            self._nivel_habilidade.append(result[2])
                            self._dado_habilidade.append(result[3])
                            self._adicional_por_nivel.append(result[4])
                            self._tipo_dano.append(result[5])
                        return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def carregar_habilidade(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT nome_habilidade, nivel_habilidade, dado_habilidade, adicional_por_nivel, tipo_dano FROM habilidade WHERE id_habilidade=%s;"
                    await mycursor.execute(query,(self._id_habilidade,))
                    result = await mycursor.fetchone() 
                    if result:
                        self.nome_habilidade = result[0]
                        self.nivel_habilidade = result[1]
                        self.dado_habilidade = result[2]
                        self.adicional_por_nivel = result[3]
                        self.tipo_dano = result[4]
                        return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_habilidade_banco(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "INSERT INTO habilidade (nome_habilidade, nivel_habilidade, dado_habilidade, adicional_por_nivel, tipo_dano) VALUES (%s,%s,%s,%s,%s);"
                    await mycursor.execute(query, (self.nome_habilidade, self.nivel_habilidade, self.dado_habilidade, self.adicional_por_nivel, self.tipo_dano))
                    self.d_habilidade = mycursor.lastrowid   
                    await conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            return False

    async def delete_habilidade_banco(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = """DELETE from habilidade
                    WHERE id_habilidade=%s;"""
                    await mycursor.execute(query, (self._id_habilidade,))
                    await conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_habilidade_banco(self, chave, valor):
        try:
            possiveis_chave = ['nome_habilidade', 'nivel_habilidade', 'dado_habilidade', 'adicional_por_nivel', 'tipo_dano']
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    if chave in possiveis_chave:
                        query = f"""UPDATE habilidade SET {chave}=%s WHERE id_habilidade=%s"""
                        await mycursor.execute(query, (valor, self._id_habilidade))
                        await conn.commit()
                        return True
        except pymysql.Error as e:
            print(e)
            return False 
        
    @property
    def nome_habilidade(self):
        return self._nome_habilidade
    
    @nome_habilidade.setter
    def nome_habilidade(self, value):
        self._nome_habilidade = value
    
    @property
    def id_habilidade(self):
        return self._id_habilidade
    
    @id_habilidade.setter
    def id_habilidade(self, value):
        self._id_habilidade = value
        
    @property
    def tipo_dano(self):
        return self._tipo_dano
    
    @tipo_dano.setter
    def tipo_dano(self, value):
        self._tipo_dano = value
        
    @property
    def dado_habilidade(self):
        return self._dado_habilidade
    
    @dado_habilidade.setter
    def dado_habilidade(self, value):
        self._dado_habilidade = value 
    
    @property
    def adicional_por_nivel(self):
        return self._adicional_por_nivel
    
    @adicional_por_nivel.setter
    def adicional_por_nivel(slef, value):
        self._adicional_por_nivel = value
        
    @property
    def nivel_habilidade(self):
        return self._nivel_habilidade
    
    @nivel_habilidade.setter
    def nivel_habilidade(self, value):
        self._nivel_habilidade = value