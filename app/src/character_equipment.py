import asyncio

from src import Character, Image, Db

class CharacterEquipment(Character, Image):
    def __init__(self, user_id=None,character_id=None, equipment_id = None, amount = None):
        super().__init__(user_id=user_id, character_id=character_id)
        Image().__init__(parameters=None)
        self.__equipment_id = equipment_id
        self.__amount = amount
        self._equipments = []
    
    async def exists_specific_equipment(self):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_equipment_id FROM character_equipment WHERE equipment_id = %s and character_id = %s)"
                parameters = (self.__equipment_id,self.character_id,)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def exists_equipment(self):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_equipment_id FROM character_equipment WHERE character_id = %s)"
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def insert_equipment(self):
        try:
            if self.character_id:
                query = "INSERT INTO character_equipment(equipment_id, character_id, amount) VALUES(%s,%s,%s);"
                parameters = (self.__equipment_id, self.character_id, self.__amount)
                db = Db()
                await db.connection_db()
                await db.insert(query=query, parameters=parameters)
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def update_equipment(self):
        try:
            if self.character_id:
                query = f"""UPDATE character_equipment
                SET amount=%s
                WHERE character_equipment_id=%s;"""
                parameters = (self.__amount, self.__equipment_id)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def delete_equipment(self):
        try:
            if self.character_id:
                query = """DELETE from character_equipment
                WHERE equipment_id=%s and character_id = %s;"""
                parameters = (self.__equipment_id, self.character_id)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_equipments(self):
        try:
            if self.character_id:
                query = """SELECT eq.kind_equipment_id, eq.equipment_name, eq.description_equipment, eq.price, eq.weight, eq.armor_class, eq.amount_dice, eq.side_dice, eq.bonus, eq.equipment_id, ke.kind_equipment_name, ce.character_equipment_id, ce.amount, eq.equipment_image, cn.coin_name, td.type_damage_name
                FROM equipment eq
                JOIN kind_equipment ke ON eq.kind_equipment_id = ke.kind_equipment_id
                JOIN character_equipment ce ON ce.equipment_id = eq.equipment_id
                JOIN coin cn ON cn.coin_id = eq.coin_id
                JOIN type_damage td ON eq.type_damage_id = td.type_damage_id
                WHERE ce.character_id = %s;"""
                await mycursor.execute(query, )
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    for row in result:
                        self.name = row[13]
                        self.equipment={
                            'kind_equipment_id': row[0],
                            'equipment_name': row[1], 
                            'description_equipment': row[2], 
                            'price': row[3],
                            'weight': row[4],
                            'armor_class': row[5],
                            'amount_dice': row[6],
                            'side_dice': row[7],
                            'bonus': row[8],
                            'equipment_id': row[9],
                            'kind_equipment_name': row[10],
                            'character_equipment_id': row[11],
                            'amount': row[12] if row[12] is not None else '',
                            'equipment_image': self.url_img,
                            'coin_name': row[14],
                            'type_damage_name': row[15]
                        }
                    return True
            return False
        except Exception as e:
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