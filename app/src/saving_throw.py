from data import get_connection
import pymysql
import asyncio

class SavingThrow:
    def __init__(self, id_saving_throw = None, saving_throw_name = None):
        self._id_saving_throw = id_saving_throw or []
        self._saving_throw_name = saving_throw_name or []
        
    @property
    def saving_throw_name(self):
        return self._saving_throw_name
    
    @property
    def id_saving_throw(self):
        return self._id_saving_throw
    
    @property
    async def saving_throws(self):
        if (type(self._id_saving_throw) is list and len(self._id_saving_throw)<=0) or (self._id_saving_throw is None):
            await self.load_saving_throws()
        salvaguardas = []
        for id_salvaguarda, nome_salvaguarda in zip(self._id_saving_throw, self._saving_throw_name):
            salvaguardas.append({'id_salvaguarda': id_salvaguarda, 'nome_salvaguarda': nome_salvaguarda})
        return salvaguardas
    
    async def load_saving_throws(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT id_salvaguarda, nome_salvaguarda FROM salvaguarda;"
                        await mycursor.execute(query)
                        result = await mycursor.fetchall() 
                        if result:
                            for row in result:
                                self._id_saving_throw.append(row[0])
                                self._saving_throw_name.append(row[1])
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_saving_throw(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT nome_salvaguarda FROM salvaguarda WHERE id_salvaguarda=%s;"
                        await mycursor.execute(query,(self._id_saving_throw,))
                        result = await mycursor.fetchall() 
                        if result:
                            self._saving_throw_name=result[0]
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_saving_throw_by_name(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT id_salvaguarda,nome_salvaguarda FROM salvaguarda WHERE nome_salvaguarda=%s;"
                        await mycursor.execute(query,(self._saving_throw_name,))
                        result = await mycursor.fetchone() 
                        if result:
                            self._id_saving_throw=result[0]
                            self._saving_throw_name=result[1]
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_saving_throw(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO salvaguarda (nome_salvaguarda) VALUES (%s);"
                        await mycursor.execute(query, (str(self._saving_throw_name),))
                        self._id_saving_throw = mycursor.lastrowid 
                        await conn.commit()
                        return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_saving_throw(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "DELETE from salvaguarda WHERE id_salvaguarda=%s;"
                        await mycursor.execute(query, (self._id_saving_throw,))
                        await conn.commit()
                        return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_saving_throw(self,valor):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "UPDATE salvaguarda SET nome_salvaguarda=%s WHERE id_salvaguarda=%s"
                        await mycursor.execute(query, (valor,self._id_saving_throw))
                        await conn.commit()
                        return True
        except pymysql.Error as e:
            print(e)
            return False        