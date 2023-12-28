from src import Character, Db

class CharacterCoin(Character):
    def __init__(self, user_id=None, character_id=None, amount_coin=None, coin_id=None):
        super().__init__(user_id, character_id)
        self.__character_coin_id = None
        self.__coin_id = coin_id
        self.__amount_coin = amount_coin
        self.__coins = []
        
    @property
    def coins(self):
        return self.__coins
    
    async def load_character_coins(self):
        try:
            if self.character_id:
                query = """SELECT cn.coin_id, cn.coin_name, CASE WHEN cc.amount_coin IS NOT NULL THEN cc.amount_coin ELSE 0 END AS amount
                FROM coin cn 
				LEFT JOIN character_coin cc ON cc.coin_id = cn.coin_id AND cc.character_id = %s;"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    self.__coins.clear()
                    for row in result:
                        self.__coins.append({'coin_id': row[0], 'coin_name': row[1], 'amount_coin': row[2]})
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def character_has_this_coin(self):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT character_coin_id FROM character_coin WHERE character_id = %s AND coin_id = %s)"
                parameters = (self.character_id, self.__coin_id)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False      

    async def insert_character_coin(self):
        try:
            if self.character_id and self.__coin_id:
                query = """
                    INSERT INTO character_coin 
                    (character_id, coin_id, amount_coin)
                    VALUES (%s, %s, %s) RETURNING character_coin_id;
                """
                parameters = (self.character_id, self.__coin_id, self.__amount_coin)
                db = Db()
                await db.connection_db()
                self.__character_coin_id = await db.insert(query=query, parameters=parameters)
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def update_character_coin(self):
        try:
            if self.character_id and self.__coin_id:
                query = f"""UPDATE character_coin
                SET amount_coin = %s
                WHERE coin_id = %s AND character_id = %s;"""
                parameters = (self.__amount_coin, self.__coin_id, self.character_id)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def delete_character_coin(self):
        try:
            if self.character_id:
                query = """DELETE FROM character_coin
                WHERE coin_id = %s AND character_id = %s;"""
                parameters = (self.__coin_id, self.character_id)
                db = Db()
                await db.connection_db()
                return db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        