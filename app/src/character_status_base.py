import asyncio

from src import Character, Db

class CharacterStatusBase(Character):
    def __init__(self, user_id=None,character_id=None):
        super().__init__(user_id=user_id, character_id=character_id)
        self._alignment = None
        self._antecedent = None
        self._ca = None
        self._displacement = None
        self._faction = None
        self._inspiration = None
        self._initiative = None
        self._level = None
        self._life = None
        self._current_life = None
        self._temporary_life = None
        self._xp = None
    
    def valid_key(self, key):
        possible_keys=['level','alignment','faction','background','experience_points','movement','initiative','hit_points','current_hit_points','temporary_hit_points','inspiration','armor_class']
        return key in possible_keys
        
    async def exists_status_base(self):
        try:
            if self.character_id:
                query = "SELECT EXISTS (SELECT status_base_id FROM status_base WHERE character_id = %s)"
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                if await db.exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def insert_status_base(self,key,value):
        try:
            if self.character_id and self.valid_key(key):
                query = f"INSERT INTO status_base(character_id,{key}) VALUES(%s,%s) RETURNING status_base_id;;"
                parameters = (self.character_id,value,)
                db = Db()
                await db.connection_db()
                await db.insert(query=query, parameters=parameters)
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def delete_status_base(self):
        try:
            if self.character_id:
                query = """DELETE from status_base
                WHERE character_id=%s;"""
                parameters = (self.character_id)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_status_base(self):
        try:
            if self.character_id:
                query = """SELECT hit_points, experience_points, level, alignment, background, faction, inspiration, armor_class, initiative, movement, current_hit_points, temporary_hit_points
                FROM status_base
                WHERE character_id = %s;"""
                parameters = (self.character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters, all=False)
                if result:
                    self.hit_points = result[0]
                    self.experience_points = result[1]
                    self.level = result[2]
                    self.alignment = result[3] 
                    self.background = result[4] 
                    self.faction = result[5]  
                    self.inspiration = result[6]
                    self.armor_class = result[7]
                    self.initiative = result[8]
                    self.movement = result[9]
                    self.current_hit_points = result[10]
                    self.temporary_hit_points = result[11]     
                    return True
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def update_status_base(self,key,value):
        try:
            
            if self.character_id and self.valid_key(key):
                query = f"""UPDATE status_base
                SET {key}=%s
                WHERE character_id=%s;"""
                parameters = (value, self.character_id)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            return False
    
    @property
    def status_base(self):
        return {
            'level': self.level,
            'alignment': self.alignment,
            'faction': self.faction,
            'background': self.background,
            'experience_points': self.experience_points,
            'movement': self.movement,
            'initiative': self.initiative,
            'hit_points': self.hit_points,
            'current_hit_points': self.current_hit_points,
            'temporary_hit_points': self.temporary_hit_points,
            'inspiration': self.inspiration,
            'armor_class': self.armor_class
        }
    
    @property
    def level(self):
        return int(self._level) if self._level is not None else None 
    
    @level.setter
    def level(self,value):
        self._level=value
    
    @property
    def alignment(self):
        return self._alignment
    
    @alignment.setter
    def alignment(self,value):
        self._alignment=value
        
    @property
    def faction(self):
        return self._faction        
         
    @faction.setter
    def faction(self,value):
        self._faction=value
        
    @property
    def background(self):
        return self._antecedent        
         
    @background.setter
    def background(self,value):
        self._antecedent=value
    
    @property
    def experience_points(self):
        return self._xp
                
    @experience_points.setter
    def experience_points(self,value):
        self._xp=value
           
    @property
    def movement(self):
        return self._displacement
    
    @movement.setter
    def movement(self,value):
        self._displacement=value
        
    @property
    def initiative(self):
        return self._initiative
    
    @initiative.setter
    def initiative(self,value):
        self._initiative=value
    
    @property
    def hit_points(self):
        return self._life
    
    @hit_points.setter
    def hit_points(self,value):
        self._life=value
        
    @property
    def current_hit_points(self):
        return self._current_life
    
    @current_hit_points.setter
    def current_hit_points(self,value):
        self._current_life=value
       
    @property
    def temporary_hit_points(self):
        return self._temporary_life
    
    @temporary_hit_points.setter
    def temporary_hit_points(self,value):
        self._temporary_life=value
        
    @property
    def inspiration(self):
        return self._inspiration
    
    @inspiration.setter
    def inspiration(self,value):
        self._inspiration=value
    
    @property
    def armor_class(self):
        return self._ca
    
    @armor_class.setter
    def armor_class(self,value):
        self._ca=value