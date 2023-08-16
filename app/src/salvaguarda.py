from data import get_connection
import pymysql
import asyncio

class Salvaguarda:
    def __init__(self,id_salvaguarda=None,nome_salvaguarda=None):
        self._id_salvaguarda = id_salvaguarda if id_salvaguarda is not None else []
        self._nome_salvaguarda = nome_salvaguarda if nome_salvaguarda is not None else []
        
    @property
    def nome_salvaguarda(self):
        return self._nome_salvaguarda
    
    @property
    def id_salvaguarda(self):
        return self._id_salvaguarda
    
    @property
    async def salvaguardas(self):
        if (type(self._id_salvaguarda) is list and len(self._id_salvaguarda)<=0) or (self._id_salvaguarda is None):
            await self.carregar_salvaguardas()
        salvaguardas = []
        for id_salvaguarda, nome_salvaguarda in zip(self._id_salvaguarda, self._nome_salvaguarda):
            salvaguardas.append({'id_salvaguarda': id_salvaguarda, 'nome_salvaguarda': nome_salvaguarda})
        return salvaguardas
    
    async def carregar_salvaguardas(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT id_salvaguarda, nome_salvaguarda FROM salvaguarda;"
                        await mycursor.execute(query)
                        result = await mycursor.fetchall() 
                        if result:
                            for row in result:
                                self._id_salvaguarda.append(row[0])
                                self._nome_salvaguarda.append(row[1])
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def carregar_salvaguarda(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT nome_salvaguarda FROM salvaguarda WHERE id_salvaguarda=%s;"
                        await mycursor.execute(query,(self._id_salvaguarda,))
                        result = await mycursor.fetchall() 
                        if result:
                            self._nome_salvaguarda=result[0]
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def carregar_salvaguarda_nome(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT id_salvaguarda,nome_salvaguarda FROM salvaguarda WHERE nome_salvaguarda=%s;"
                        await mycursor.execute(query,(self._nome_salvaguarda,))
                        result = await mycursor.fetchone() 
                        if result:
                            self._id_salvaguarda=result[0]
                            self._nome_salvaguarda=result[1]
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_salvaguarda_banco(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO salvaguarda (nome_salvaguarda) VALUES (%s);"
                        await mycursor.execute(query, (str(self._nome_salvaguarda),))
                        self._id_salvaguarda = await mycursor.lastrowid 
                        await conn.commit()
                        return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_salvaguarda_banco(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "DELETE from salvaguarda WHERE id_salvaguarda=%s;"
                        await mycursor.execute(query, (self._id_salvaguarda,))
                        await conn.commit()
                        return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_salvaguarda_banco(self,valor):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "UPDATE salvaguarda SET nome_salvaguarda=%s WHERE id_salvaguarda=%s"
                        await mycursor.execute(query, (valor,self._id_salvaguarda))
                        await conn.commit()
                        return True
        except pymysql.Error as e:
            print(e)
            return False        