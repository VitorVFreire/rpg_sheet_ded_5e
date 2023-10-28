from data import get_connection
import pymysql
import asyncio

class Race:
    def __init__(self,id_race=None,race_name=None):
        self._id_race = id_race or[]
        self._race_name = race_name or []
        
    @property
    def race_name(self):
        return self._race_name
    
    @property
    def id_race(self):
        return self._id_race
    
    @property
    async def races(self):
        if (type(self._id_race) is list and len(self._id_race)<=0) or (self._id_race is None):
            await self.load_races()
        racas = []
        for id_raca, nome_raca in zip(self._id_race, self._race_name):
            racas.append({'id_raca': id_raca, 'nome_raca': nome_raca})
        return racas
    
    async def load_races(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_raca, nome_raca FROM raca;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        for row in result:
                            self._id_race.append(row[0])
                            self._race_name.append(row[1])
                        await conn.close()
                        return True
                    await conn.close()
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_race(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT nome_raca FROM raca WHERE id_raca=%s;"
                    await mycursor.execute(query,(self._id_race,))
                    result = await mycursor.fetchall() 
                    if result:
                        self._race_name=result[0]
                        await conn.close()
                        return True
                    await conn.close()
            return False
        except Exception as e:
            print(e)
            return False
        
    async def insert_race(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "INSERT INTO raca (nome_raca) VALUES (%s);"
                    await mycursor.execute(query, (str(self._race_name),))
                    self._id_race = mycursor.lastrowid 
                    await conn.commit()
                    await conn.close()
                    return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_race(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "DELETE from raca WHERE id_raca=%s;"
                    await mycursor.execute(query, (self._id_race,))
                    await conn.commit()
                    await conn.close()
                    return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_race(self,valor):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "UPDATE raca SET nome_raca=%s WHERE id_raca=%s"
                    await mycursor.execute(query, (valor,self._id_race))
                    await conn.commit()
                    await conn.close()
                    return True
        except pymysql.Error as e:
            print(e)
            return False        