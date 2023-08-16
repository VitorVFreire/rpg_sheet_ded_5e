from data import get_connection
import pymysql
import asyncio

class Raca:
    def __init__(self,id_raca=None,nome_raca=None):
        self._id_raca = id_raca if id_raca is not None else []
        self._nome_raca = nome_raca if nome_raca is not None else []
        
    @property
    def nome_raca(self):
        return self._nome_raca
    
    @property
    def id_raca(self):
        return self._id_raca
    
    @property
    async def racas(self):
        if (type(self._id_raca) is list and len(self._id_raca)<=0) or (self._id_raca is None):
            await self.carregar_racas()
        racas = []
        for id_raca, nome_raca in zip(self._id_raca, self._nome_raca):
            racas.append({'id_raca': id_raca, 'nome_raca': nome_raca})
        return racas
    
    async def carregar_racas(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_raca, nome_raca FROM raca;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        for row in result:
                            self._id_raca.append(row[0])
                            self._nome_raca.append(row[1])
                        await conn.close()
                        return True
                    await conn.close()
            return False
        except Exception as e:
            print(e)
            return False
        
    async def carregar_raca(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT nome_raca FROM raca WHERE id_raca=%s;"
                    await mycursor.execute(query,(self._id_raca,))
                    result = await mycursor.fetchall() 
                    if result:
                        self._nome_raca=result[0]
                        await conn.close()
                        return True
                    await conn.close()
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_raca_banco(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "INSERT INTO raca (nome_raca) VALUES (%s);"
                    await mycursor.execute(query, (str(self._nome_raca),))
                    self._id_raca = await mycursor.lastrowid 
                    await conn.commit()
                    await conn.close()
                    return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_raca_banco(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "DELETE from raca WHERE id_raca=%s;"
                    await mycursor.execute(query, (self._id_raca,))
                    await conn.commit()
                    await conn.close()
                    return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_raca_banco(self,valor):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "UPDATE raca SET nome_raca=%s WHERE id_raca=%s"
                    await mycursor.execute(query, (valor,self._id_raca))
                    await conn.commit()
                    await conn.close()
                    return True
        except pymysql.Error as e:
            print(e)
            return False        