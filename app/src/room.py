from flask import abort
from src import Db

class Room:
    def __init__(self, room_id=None, character_id=None, user_id=None, room_name=None, user_room_id=None, room_password=None, room_image=None):
        self.__room_id = room_id or []
        self.__room_name = room_name or []
        self.__room_password = room_password or []
        self._character_id = character_id
        self.__user_id = user_id
        self.__user_room_id = user_room_id
        self.__room_image = room_image
    
    @property    
    def roons(self):
        roons = []
        for room_id, room_name in zip(self.__room_id, self.__room_name):
            roons.append({'room_id': room_id, 'room_name': room_name})
        return roons      
    
    @property
    def room_id(self):
        return self.__room_id
    
    @property
    def room_name(self):
        return self.__room_name
        
    def exists_user_room(self):
        try:
            if self._character_id:   
                query = "SELECT EXISTS (SELECT user_room_id FROM user_room WHERE user_id = %s and room_id = %s)"
                parameters = (self._character_id, self.__room_id,)
                db = Db()
                db.sync_connection_db()
                if db.sync_exists(query=query, parameters=parameters):
                    return True
            return False
        except Exception as e:
            print(e)
            abort(500)
        
    def load_user_room(self):
        try:
            if self._character_id: 
                query = "SELECT rm.room_id, rm.room_name  FROM user_room ur, room rm WHERE ur.user_id = %s and ur.room_id = rm.room_id;"
                parameters = (self._character_id,)
                db = Db()
                db.sync_connection_db()
                result = db.select(query=query, parameters=parameters)
                if result:
                    for row in result:
                        self.__room_id.append(row[0])
                        self.__room_name.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            abort(500)
                                                                                                                                                                                                                                                                                                          
    def insert_user_room(self):
        try:
            if self._character_id and self.exists_user_room() is False:    
                query = """INSERT INTO user_room
                    (user_id, room_id, user_room_type) 
                    VALUES(%s,%s,0);"""
                parameters = (self._character_id, self.__room_id)
                db = Db()
                db.sync_connection_db()
                self.__user_room_id = db.sync_insert(query=query, parameters=parameters)  
                return True
            return False
        except Exception as e:
            print(e)
            abort(500, 'Erro na inserção ao banco')
        
    def insert_room(self):
        try:
            if self.__user_id:    
                query = """INSERT INTO room
                    (user_id, room_name, room_password) 
                    VALUES(%s,%s,%s);"""
                parameters = (self.__user_id, self.__room_name, self.__room_password)
                db = Db()
                db.sync_connection_db()
                self.__room_id[0] = db.sync_insert(query=query, parameters=parameters)  
                return True
            return False
        except Exception as e:
            print(e)
            abort(500, 'Erro na inserção ao banco')
            
    def delete_room(self):
        try:    
            query = "DELETE FROM room WHERE room_id = %s"
            parameters = (self.__room_id,)
            db = Db()
            db.sync_connection_db()
            return db.sync_delete(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            abort(500, 'Erro na exclusão da sala')
    
    def update_room(self):
        try:    
            query = "UPDATE room SET room_name = %s WHERE room_id = %s"
            parameters = (self.__room_name,self.__room_id,)
            db = Db()
            db.sync_connection_db()
            return db.sync_update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            abort(500, 'Erro na exclusão da sala')
            
    def delete_user_room(self):
        try:
            if self.__user_id:    
                query = "DELETE FROM user_room WHERE room_id = %s and user_id = %s"
                parameters = (self.__room_id, self._character_id)(self.__user_id, self.__room_name, self.__room_password)
                db = Db()
                db.sync_connection_db()
                return db.sync_delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            abort(500, 'Erro na exclusão da sala')