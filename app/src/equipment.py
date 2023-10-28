from data import get_connection
import pymysql
import asyncio
from flask import url_for

from src import Image

class Equipment(Image):
    def __init__(self, id_equipment = None, id_equipment_type = None, equipment_type_name = None, equipment_name = None, description = None, price = None, weight = None, ca = None, dice = None, bonus = None, name = None, equipment_image = None):
        super().__init__(parameters=id_equipment,name=name)
        self.__id_equipment_type = [id_equipment_type]
        self.__equipment_type_name = [equipment_type_name]
        self.__id_equipment = [id_equipment]
        self.__equipment_name = [equipment_name]
        self.__description = [description]
        self.__price = [price]
        self.__weight = [weight]
        self.__ca = [ca]
        self.__dice = [dice]
        self.__bonus = [bonus]
        self.__equipment_image = [equipment_image]
        self.__character_equipments = []
    
    @property
    def equipment_image(self):
        return self.__equipment_image
            
    @equipment_image.setter
    def equipment_image(self, value):
        self.name = value
        self.__equipment_image.append(self.url_img)
        
    @property
    def equipments(self):
        equipments = []
        for id_equipment_type, equipment_type_name, id_equipment, equipment_name, description, price, weight, ca, dice, bonus, equipment_image in zip(self.__id_equipment_type, self.__equipment_type_name, self.__id_equipment, self.__equipment_name, self.__description, self.__price, self.__weight, self.__ca, self.__dice, self.__bonus, self.equipment_image):
            equipments.append({
                'id_tipo_equipamento': id_equipment_type, 
                'nome_tipo_equipamento': equipment_type_name,
                'id_equipamento': id_equipment, 
                'nome_equipamento': equipment_name, 
                'descricao': description,  
                'preco': price, 
                'peso': weight, 
                'ca': ca,
                'dado': dice,
                'bonus': bonus,
                'imagem_equipamento': equipment_image,
                'personagem_possui': id_equipment in self.__character_equipments
            })
        return equipments if equipments[0]['id_equipamento'] is not None else None
    
    @property
    def equipment(self):
        equipment = {
            'id_tipo_equipamento': self.id_equipment_type, 
            'nome_tipo_equipamento': self.__equipment_type_name,
            'id_equipamento': self.id_equipment, 
            'nome_equipamento': self.equipment_name, 
            'descricao': self.description,  
            'preco': self.price, 
            'peso': self.weight, 
            'ca': self.ca,
            'dado': self.dice,
            'bonus': self.bonus,
            'imagem_equipamento': self.equipment_image,
            'personagem_possui': self.__id_equipment in self.__character_equipments
        }
        return equipment if equipment['id_equipamento'] is not None else None
    
    def equipment_clear(self):
        if self.__id_equipment[0] is None:
            self.__id_equipment_type.clear()
            self.__equipment_type_name.clear()
            self.__id_equipment.clear()
            self.__equipment_name.clear()
            self.__description.clear()
            self.__price.clear()
            self.__weight.clear()
            self.__ca.clear()
            self.__dice.clear()
            self.__bonus.clear()
            self.__equipment_image.clear()

    @property
    def type_equipments(self):
        tipo_equipamento = []
        for id_tipo_equipamento, nome_tipo_equipamento in zip(self.__id_equipment_type, self.__equipment_type_name):
            tipo_equipamento.append({
                'id_tipo_equipamento': id_tipo_equipamento, 
                'nome_tipo_equipamento': nome_tipo_equipamento
            })
        return tipo_equipamento
    
    async def load_type_equipment(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_tipo_equipamento, nome_tipo_equipamento FROM tipo_equipamento;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        self.equipment_clear()
                        for row in result:
                            self.__id_equipment_type.append(row[0])
                            self.__equipment_type_name.append(row[1])
                        return True
            return False
        except Exception as e:
            print(e)
            return False

    async def load_character_equipments(self, id_personagem):
        try:
            if id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT id_equipamento FROM equipamento_personagem WHERE id_personagem = %s;"""
                        await mycursor.execute(query, (id_personagem,))
                        result = await mycursor.fetchall()
                        if result:
                            for row in result:
                                self.__character_equipments.append(row[0])              
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
   
    async def load_equipments(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT eq.id_tipo_equipamento, eq.nome_equipamento, eq.descricao, eq.preco, eq.peso, eq.ca, eq.dado, eq.bonus, eq.id_equipamento, te.nome_tipo_equipamento, eq.imagem_equipamento FROM equipamento eq, tipo_equipamento te WHERE eq.id_tipo_equipamento = te.id_tipo_equipamento;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        self.equipment_clear()
                        for row in result:
                            self.__id_equipment_type.append(row[0])
                            self.__equipment_name.append(row[1]) 
                            self.__description.append(row[2]) 
                            self.__price.append(row[3])
                            self.__weight.append(row[4])
                            self.__ca.append(row[5])
                            self.__dice.append(row[6])
                            self.__bonus.append(row[7])
                            self.__id_equipment.append(row[8])
                            self.__equipment_type_name.append(row[9])
                            self.equipment_image = row[10]
                        return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def load_equipment(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_tipo_equipamento, nome_equipamento, descricao, preco, peso, ca, dado, bonus, imagem_equipamento FROM equipamento WHERE id_equipamento=%s;"
                    await mycursor.execute(query,(self.id_equipment,))
                    result = await mycursor.fetchone() 
                    if result:
                        self.equipment_clear()
                        self.__id_equipment_type.append(result[0])
                        self.__equipment_name.append(result[1]) 
                        self.__description.append(result[2]) 
                        self.__price.append(result[3])
                        self.__weight.append(result[4])
                        self.__ca.append(result[5])
                        self.__dice.append(result[6])
                        self.__bonus.append(result[7])
                        self.equipment_image(result[8])
                        return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_equipment(self):
        try:
            if self.__id_equipment_type:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        self.__equipment_image[0] = self.save_equipment_image(self.equipment_image) if self.equipment_image is not None else None
                        query = "INSERT INTO equipamento (id_tipo_equipamento, nome_equipamento, descricao, preco, peso, ca, dado, bonus, imagem_equipamento) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                        await mycursor.execute(query, (self.id_equipment_type, self.equipment_name, self.description, self.price, self.weight, self.ca, self.dice, self.bonus, self.equipment_image))
                        self.__id_equipment[0] = mycursor.lastrowid   
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            self.name = self.equipment_image
            self.remove_file()
            print(e)
            return False

    async def delete_equipment(self):
        try:
            if self.__id_equipment:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from equipamento
                        WHERE id_equipamento=%s;"""
                        await mycursor.execute(query, (self.id_equipment,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_equipment(self, chave, valor):
        try:
            possiveis_chave = ['id_tipo_equipamento', 'nome_equipamento', 'descricao', 'preco', 'peso', 'ca', 'dado', 'bonus', 'imagem_equipamento']
            if chave in possiveis_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE equipamento SET {chave}=%s WHERE id_equipamento=%s"""
                        await mycursor.execute(query, (valor, self.id_equipment))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False 
    
    def save_equipment_image(self, file):
        try:
            self.parameter = 'equipamento'
            result, name = self.save_file(file) 
            return name if result is True else None
        except Exception as e:
            print(e)
            return False       
        
    @property
    def ca(self):
        if isinstance(self.__ca, list) and self.__ca[0] == '':
            return None
        return self.__ca[0]
    
    @property
    def id_equipment(self):
        if isinstance(self.__id_equipment, list) and self.__id_equipment[0] == '':
            return None
        return self.__id_equipment[0]
    
    @property
    def id_equipment_type(self):
        if isinstance(self.__id_equipment_type, list) and self.__id_equipment_type[0] == '':
            return None
        return self.__id_equipment_type[0]
    
    @property
    def equipment_type_name(self):
        if isinstance(self.__equipment_type_name, list) and self.__equipment_type_name[0] == '':
            return None
        return self.__equipment_type_name[0]
    
    @property
    def equipment_name(self):
        if isinstance(self.__equipment_name, list) and self.__equipment_name[0] == '':
            return None
        return self.__equipment_name[0]
    
    @property
    def description(self):
        if isinstance(self.__description, list) and self.__description[0] == '':
            return None
        return self.__description[0]
    
    @property
    def equipment_image(self):
        if isinstance(self.__equipment_image, list) and self.__equipment_image[0] == '':
            return None
        return self.__equipment_image[0]
    
    @property
    def price(self):
        if isinstance(self.__price, list) and self.__price[0] == '':
            return None
        return self.__price[0]
    
    @property
    def weight(self):
        if isinstance(self.__weight, list) and self.__weight[0] == '':
            return None
        return self.__weight[0]
    
    @property
    def dice(self):
        if isinstance(self.__dice, list) and self.__dice[0] == '':
            return None
        return self.__dice[0]
    
    @property
    def bonus(self):
        if isinstance(self.__bonus, list) and self.__bonus[0] == '':
            return None
        return self.__bonus[0]
    