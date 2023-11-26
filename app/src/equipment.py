import asyncio
from flask import url_for

from src import Image, Db

def bool_id(id, data):
    return id in data

class Equipment(Image):
    def __init__(self, equipment_id = None, kind_equipment_id = None, kind_equipment_name = None, equipment_name = None, description_equipment = None, price = None, weight = None, armor_class = None, amount_dice = None, side_dice = None, bonus = None, name = None, equipment_image = None, type_damage_id = None, coin_id = None):
        super().__init__(parameters=equipment_id,name=name)
        self.__kind_equipment_id = [kind_equipment_id]
        self.__kind_equipment_name = [kind_equipment_name]
        self.__equipment_id = [equipment_id]
        self.__equipment_name = [equipment_name]
        self.__description_equipment = [description_equipment]
        self.__price = [price]
        self.__weight = [weight]
        self.__armor_class = [armor_class]
        self.__amount_dice = [amount_dice]
        self.__side_dice = [side_dice]
        self.__bonus = [bonus]
        self.__equipment_image = [equipment_image]
        self.__coin_name = []
        self.__type_damage_name = []
        self.__character_equipments = []
        self.__coin_id = coin_id
        self.__type_damage_id = type_damage_id
    
    @property
    def equipment_image(self):
        return self.__equipment_image
            
    @equipment_image.setter
    def equipment_image_set(self, value):
        self.name = value
        self.__equipment_image.append(self.url_img)
        
    @property
    def equipments(self):
        equipments = []
        for kind_equipment_id, kind_equipment_name, equipment_id, equipment_name, description_equipment, price, weight, armor_class, amount_dice, side_dice, bonus, equipment_image, type_damage_name, coin_name in zip(self.__kind_equipment_id, self.__kind_equipment_name, self.__equipment_id, self.__equipment_name, self.__description_equipment, self.__price, self.__weight, self.__armor_class, self.__amount_dice, self.__side_dice, self.__bonus, self.equipment_image, self.__type_damage_name, self.__coin_name):
            equipments.append({
                'kind_equipment_id': kind_equipment_id, 
                'kind_equipment_name': kind_equipment_name,
                'equipment_id': equipment_id, 
                'equipment_name': equipment_name, 
                'description_equipment': description_equipment,  
                'price': price, 
                'weight': weight, 
                'armor_clas': armor_class,
                'amount_dice': amount_dice,
                'side_dice': side_dice,
                'bonus': bonus,
                'equipment_image': equipment_image,
                'coin_name': coin_name,
                'type_damage_name': type_damage_name,
                'character_has': any(equipment_id == equipment['equipment_id'] for equipment in self.__character_equipments),
                'amount': [amount['amount'] if equipment_id == amount['equipment_id'] else 0 for amount in self.__character_equipments][0]
            })

        return equipments if equipments is not None else None
    
    @property
    def equipment(self):
        equipment = {
            'kind_equipment_id': self.kind_equipment_id, 
            'kind_equipment_name': self.__kind_equipment_name,
            'equipment_id': self.equipment_id, 
            'equipment_name': self.equipment_name, 
            'description_equipment': self.description_equipment,  
            'price': self.price, 
            'weight': self.weight, 
            'armor_class': self.armor_class,
            'amount_dice': self.amount_dice,
            'side_dice': self.side_dice,
            'bonus': self.bonus,
            'coin_name': self.coin_name,
            'type_damage_name': self.type_damage_name,
            'equipment_image': self.equipment_image,
            'character_has': self.__equipment_id in self.__character_equipments[0]['equipment_id'],
            'amount_equipments': self.__character_equipments[0]['amount'] if self.__equipment_id in self.__character_equipments[0]['equipment_id'] else 0
        }
        return equipment if equipment['equipment_id'] is not None else None
    
    def equipment_clear(self):
        if self.__equipment_id[0] is None:
            self.__kind_equipment_id.clear()
            self.__kind_equipment_name.clear()
            self.__equipment_id.clear()
            self.__equipment_name.clear()
            self.__description_equipment.clear()
            self.__price.clear()
            self.__weight.clear()
            self.__armor_class.clear()
            self.__amount_dice.clear()
            self.__side_dice.clear()
            self.__bonus.clear()
            self.__equipment_image.clear()
            self.__kind_equipment_name = []
            self.__coin_name = []

    @property
    def type_equipments(self):
        kind_equipment = []
        for kind_equipment_id, kind_equipment_name in zip(self.__kind_equipment_id, self.__kind_equipment_name):
            kind_equipment.append({
                'kind_equipment_id': kind_equipment_id, 
                'kind_equipment_name': kind_equipment_name
            })
        return kind_equipment
    
    async def load_type_equipment(self):
        try:
            query = "SELECT kind_equipment_id, kind_equipment_name FROM kind_equipment;"
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                self.equipment_clear()
                for row in result:
                    self.__kind_equipment_id.append(row[0])
                    self.__kind_equipment_name.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False

    async def load_character_equipments(self, character_id):
        try:
            if character_id:
                query = """SELECT equipment_id, amount FROM character_equipment WHERE character_id = %s;"""
                parameters = (character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    for row in result:
                        self.__character_equipments.append({'equipment_id': row[0], 'amount': row[1]}) 
                    return True
            return False
        except Exception as e:
            print(e)
            return False
   
    async def load_equipments(self):
        try:
            query = """SELECT eq.kind_equipment_id, eq.equipment_name, eq.description_equipment, eq.price, eq.weight, eq.armor_class, eq.amount_dice, eq.side_dice, eq.bonus, eq.equipment_id, te.kind_equipment_name, eq.equipment_image, td.type_damage_name, cn.coin_name 
            FROM equipment eq
            JOIN kind_equipment te ON eq.kind_equipment_id = te.kind_equipment_id
            LEFT JOIN type_damage td ON td.type_damage_id = eq.type_damage_id
            JOIN coin cn ON cn.coin_id = eq.coin_id;"""
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                self.equipment_clear()
                for row in result:
                    self.__kind_equipment_id.append(row[0])
                    self.__equipment_name.append(row[1]) 
                    self.__description_equipment.append(row[2]) 
                    self.__price.append(row[3])
                    self.__weight.append(row[4])
                    self.__armor_class.append(row[5])
                    self.__amount_dice.append(row[6])
                    self.__side_dice.append(row[7])
                    self.__bonus.append(row[8])
                    self.__equipment_id.append(row[9])
                    self.__kind_equipment_name.append(row[10])
                    self.equipment_image_set = row[11]
                    self.__type_damage_name.append(row[12])
                    self.__coin_name.append(row[13])
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def load_equipment(self):
        try:
            query = """SELECT eq.kind_equipment_id, eq.equipment_name, eq.description_equipment, eq.price, eq.weight, eq.armor_class, eq.amount_dice, eq.side_dice, eq.bonus, te.kind_equipment_name, eq.equipment_image, td.type_damage_name, cn.coin_name 
            FROM equipment eq
            JOIN kind_equipment te ON eq.kind_equipment_id = te.kind_equipment_id
            LEFT JOIN type_damage td ON td.type_damage_id = eq.type_damage_id
            JOIN coin cn ON cn.coin_id = eq.coin_id
            WHERE eq.equipment_id = %s;"""
            parameters = (self.equipment_id,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self.equipment_clear()
                self.__kind_equipment_id.append(result[0])
                self.__equipment_name.append(result[1]) 
                self.__description_equipment.append(result[2]) 
                self.__price.append(result[3])
                self.__weight.append(result[4])
                self.__armor_class.append(result[5])
                self.__amount_dice.append(result[6])
                self.__side_dice.append(result[7])
                self.__bonus.append(result[8])
                self.__kind_equipment_name.append(result[9])
                self.equipment_image_set(result[10])
                self.__type_damage_name.append(result[11])
                self.__coin_name.append(result[12])
                return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_equipment(self):
        try:
            if self.kind_equipment_id:
                self.__equipment_image[0] = self.save_equipment_image(self.equipment_image) if self.equipment_image is not None else None
                query = "INSERT INTO equipment (kind_equipment_id, equipment_name, description_equipment, price, weight, armor_class, amount_dice, side_dice, bonus, equipment_image, type_damage_id, coin_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING equipment_id;"
                parameters = (self.kind_equipment_id, self.equipment_name, self.description_equipment, self.price, self.weight, self.armor_class, self.amount_dice, self.side_dice, self.bonus, self.equipment_image, self.type_damage_id, self.__coin_id)
                db = Db()
                await db.connection_db()
                self.__equipment_id[0] = await db.insert(query=query, parameters=parameters)   
                print(self.__equipment_id)
                return True
            return False
        except Exception as e:
            self.name = self.equipment_image
            self.remove_file()
            print(e)
            return False

    async def delete_equipment(self):
        try:
            if self.equipment_id:
                query = """DELETE from equipment
                WHERE equipment_id=%s;"""
                parameters = (self.equipment_id,)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def update_equipment(self, key, value):
        try:
            possiveis_key = ['kind_equipment_id', 'equipment_name', 'description_equipment', 'price', 'weight', 'armor_class', 'amount_dice', 'side_dice', 'bonus', 'equipment_image', 'type_damage_id', 'coin_id']
            if key in possiveis_key:
                query = f"""UPDATE equipment SET {key}=%s WHERE equipment_id=%s"""
                parameters = (value, self.equipment_id)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False 
    
    def save_equipment_image(self, file):
        try:
            self.parameter = 'equipment'
            result, name = self.save_file(file) 
            return name if result is True else None
        except Exception as e:
            print(e)
            return False       
        
    @property
    def armor_class(self):
        if isinstance(self.__armor_class, list) and self.__armor_class[0] == '':
            return None
        return self.__armor_class[0]
    
    @property
    def equipment_id(self):
        if isinstance(self.__equipment_id, list) and self.__equipment_id[0] == '':
            return None
        return self.__equipment_id[0]
    
    @property
    def kind_equipment_id(self):
        if isinstance(self.__kind_equipment_id, list) and self.__kind_equipment_id[0] == '':
            return None
        return self.__kind_equipment_id[0]
    
    @property
    def kind_equipment_name(self):
        if isinstance(self.__kind_equipment_name, list) and self.__kind_equipment_name[0] == '':
            return None
        return self.__kind_equipment_name[0]
    
    @property
    def equipment_name(self):
        if isinstance(self.__equipment_name, list) and self.__equipment_name[0] == '':
            return None
        return self.__equipment_name[0]
    
    @property
    def description_equipment(self):
        if isinstance(self.__description_equipment, list) and self.__description_equipment[0] == '':
            return None
        return self.__description_equipment[0]
    
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
    def amount_dice(self):
        if isinstance(self.__amount_dice, list) and self.__amount_dice[0] == '':
            return None
        return self.__amount_dice[0]
    
    @property
    def side_dice(self):
        if isinstance(self.__side_dice, list) and self.__side_dice[0] == '':
            return None
        return self.__side_dice[0]
    
    @property
    def bonus(self):
        if isinstance(self.__bonus, list) and self.__bonus[0] == '':
            return None
        return self.__bonus[0]
    
    @property
    def type_damage_name(self):
        if isinstance(self.__type_damage_name, list) and self.__type_damage_name[0] == '':
            return None
        return self.__type_damage_name[0]
    
    @property
    def coin_name(self):
        if isinstance(self.__coin_name, list) and self.__coin_name[0] == '':
            return None
        return self.__coin_name[0]
    
    @property
    def type_damage_id(self):
        if isinstance(self.__type_damage_id, list) or self.__type_damage_id == '':
            return None
        return self.__type_damage_id[0]
    