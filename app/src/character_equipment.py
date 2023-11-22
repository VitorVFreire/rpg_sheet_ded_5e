from data import get_connection
import pymysql
import asyncio

from src import Character, Image

class CharacterEquipment(Character, Image):
    def __init__(self, user_id=None,id_character=None, id_equipment = None, amount = None):
        super().__init__(user_id=user_id, id_character=id_character)
        Image().__init__(parameters=None)
        self.__id_equipment = id_equipment
        self.__amount = amount
        self._equipments = []
    
    async def exists_specific_equipment(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_equipamento_personagem FROM equipamento_personagem WHERE id_equipamento = %s and id_personagem = %s)"
                        await mycursor.execute(query, (self.__id_equipment,self.id_character,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def exists_equipment(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_equipamento_personagem FROM equipamento_personagem WHERE id_personagem = %s)"
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def insert_equipment(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO equipamento_personagem(id_equipamento, id_personagem, qtd) VALUES(%s,%s,%s);"
                        await mycursor.execute(query, (self.__id_equipment, self.id_character, self.__amount))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def update_equipment(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE equipamento_personagem
                        SET qtd=%s
                        WHERE id_equipamento_personagem=%s;"""
                        await mycursor.execute(query, (self.__amount, self.__id_equipment))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_equipment(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from equipamento_personagem
                        WHERE id_equipamento=%s and id_personagem = %s;"""
                        await mycursor.execute(query, (self.__id_equipment, self.id_character))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def load_equipments(self):
        try:
            if self.id_character:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT eq.id_tipo_equipamento, eq.nome_equipamento, eq.descricao, eq.preco, eq.peso, eq.ca, eq.dado, eq.bonus, eq.id_equipamento, te.nome_tipo_equipamento, ep.id_equipamento_personagem, ep.qtd, eq.imagem_equipamento
                        FROM equipamento eq, tipo_equipamento te, equipamento_personagem ep 
                        WHERE eq.id_tipo_equipamento = te.id_tipo_equipamento AND ep.id_equipamento = eq.id_equipamento AND ep.id_personagem = %s;"""
                        await mycursor.execute(query, (self.id_character,))
                        result = await mycursor.fetchall() 
                        if result:
                            for row in result:
                                self.name = row[12]
                                self.equipment={
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
                                    'qtd': row[11] if row[11] is not None else '',
                                    'imagem_equipamento': self.url_img
                                }
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    def equipment(self, value):
        return self._equipments[value]
    
    @property
    def list_equipments(self):
        return self._equipments  
    
    @equipment.setter
    def equipment(self, value):
        self._equipments.append(value)