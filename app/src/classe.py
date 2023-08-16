from data import get_connection
import pymysql
import asyncio

class Classe:
    def __init__(self, id_classe=None, nome_classe=None):
        self._id_classe = [] if id_classe is None else id_classe
        self._nome_classe = nome_classe if nome_classe is not None else []
        
    @property
    def nome_classe(self):
        return self._nome_classe
    
    @property
    def id_classe(self):
        return self._id_classe

    @property
    async def classes(self):
        if (type(self._id_classe) is list and len(self._id_classe)<=0) or (self._id_classe is None):
            await self.carregar_classes()
        classes=[]
        for id_classe,nome_classe in zip(self._id_classe,self._nome_classe):
            classes.append({'id_classe':id_classe,'nome_classe':nome_classe})
        return classes
    
    async def carregar_classes(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_classe, nome_classe FROM classe;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        for row in result:
                            self._id_classe.append(row[0])
                            self._nome_classe.append(row[1])
                            return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def carregar_classe(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT nome_classe FROM classe WHERE id_classe=%s;"
                    await mycursor.execute(query,(self._id_classe,))
                    result = await mycursor.fetchall() 
                    if result:
                        self._nome_classe=result[0]
                        return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_classe_banco(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "INSERT INTO classe (nome_classe) VALUES (%s);"
                    await mycursor.execute(query, (str(self._nome_classe),))
                    self._id_classe = await mycursor.lastrowid   
                    await conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            return False

    async def delete_classe_banco(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = """DELETE from classe
                    WHERE id_classe=%s;"""
                    await mycursor.execute(query, (self._id_classe,))
                    await conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_classe_banco(self,valor):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "UPDATE classe SET nome_classe=%s WHERE id_classe=%s"
                    await mycursor.execute(query, (valor,self._id_classe))
                    await conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            return False 