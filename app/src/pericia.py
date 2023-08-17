from data import get_connection
import pymysql
import asyncio

class Pericia:
    def __init__(self,id_pericia=None,nome_pericia=None,status_uso=None):
        self._id_pericia= id_pericia if id_pericia is not None else []
        self._nome_pericia= nome_pericia if nome_pericia is not None else []
        self._status_uso= status_uso if status_uso is not None else []
        
    @property
    def nome_pericia(self):
        return self._nome_pericia
    
    @property
    def id_pericia(self):
        return self._id_pericia
    
    @property
    def status_uso(self):
        return self._status_uso
    
    @property
    async def pericias(self):
        if (type(self._id_pericia) is list and len(self._id_pericia)<=0) or (self._id_pericia is None):
            await self.carregar_pericias()
        pericias=[]
        for id_pericia,nome_pericia,status_uso in zip(self._id_pericia,self._nome_pericia,self._status_uso):
            pericias.append({'id_pericia':id_pericia,'nome_pericia':nome_pericia,'status_uso':status_uso})
        return pericias
    
    async def carregar_pericias(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT id_pericia, nome_pericia, status_uso from pericia;"
                        await mycursor.execute(query)
                        result = await mycursor.fetchall() 
                        if result:
                            for row in result:
                                self._id_pericia.append(row[0])
                                self._nome_pericia.append(row[1])
                                self._status_uso.append(row[2])
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def carregar_pericia(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT nome_pericia, status_uso FROM pericia WHERE id_pericia=%s;"
                        await mycursor.execute(query,(self._id_pericia,))
                        result = await mycursor.fetchall() 
                        if result:
                            self._nome_pericia=result[0]
                            self._status_uso=result[1]
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def carregar_pericia_nome(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT id_pericia, status_uso FROM pericia WHERE nome_pericia=%s;"
                        await mycursor.execute(query,(self._nome_pericia,))
                        result = await mycursor.fetchone() 
                        if result:
                            self._id_pericia=result[0]
                            self._status_uso=result[1]
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_pericia_banco(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO pericia(nome_pericia,status_uso) VALUES(%s,%s);"
                        await mycursor.execute(query, (self._nome_pericia,self._status_uso,))
                        self._id_pericia = await mycursor.lastrowid
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_pericia_banco(self):
        try:
            async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from pericia
                        WHERE id_pericia=%s;"""
                        await mycursor.execute(query, (self._id_pericia,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_pericia_banco(self,chave,valor):
        try:
            possiveis_chave=['nome_pericia','status_uso']
            if chave in possiveis_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"UPDATE pericia SET {chave}=%s WHERE id_pericia=%s"
                        await mycursor.execute(query, (valor,self._id_pericia,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False        