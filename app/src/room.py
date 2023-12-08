from flask import abort
from src import Db, Image

class Room:
    def __init__(self, room_id=None, user_id=None, room_name=None, user_room_id=None, room_password=None, background_cartesian_plane=None):
        self.__room_id = room_id or []
        self.__room_name = room_name or []
        self.__room_password = room_password or []
        self.__user_id = user_id
        self.__user_room_id = user_room_id or []
        self.__background_cartesian_plane = background_cartesian_plane
        self.__roons = []
        self.__error = ''
        self.__can_delete = False
        
    @property
    def background_cartesian_plane(self):
        img = Image(parameters='background')
        if self.__background_cartesian_plane is not None:
            result, name = img.save_file(self.__background_cartesian_plane)
            return name
        img.name = img.img_default_path(index=2)
        return [img.name]
    
    @property
    def error(self):
        return self.__error
    
    @property
    def can_delete(self):
        return self.__can_delete
    
    @property
    def background_cartesian_plane_load(self):
        img = Image(name=self.__background_cartesian_plane)
        if self.__background_cartesian_plane is None:
            img.name = img.img_default_path(index=2)
        return img.url_img
    
    @property    
    def roons(self):
        roons = []
        for room_id, room_name in zip(self.__room_id, self.__room_name):
            roons.append({'room_id': room_id, 'room_name': room_name})
        return roons 
    
    @property
    def room(self):
        room = {
            'room_name': self.__room_name[0],
            'room_image': self.__background_cartesian_plane[0]
        }     
        return room
    
    @property
    def room_id(self):
        return self.__room_id[0] if type(self.__room_id) is list else self.__room_id
    
    @room_id.setter
    def room_id(self, value):
        self.__room_id[0] = value
    
    @property
    def user_room_id(self):
        return self.__user_room_id[0] if type(self.__user_room_id) is list else self.__user_room_id
    
    @user_room_id.setter
    def user_room_id(self, value):
        self.__user_room_id[0] = value
    
    @property
    def room_name(self):
        return self.__room_name[0] if type(self.__room_name) is list else self.__room_name
    
    @property
    def room_password(self):
        if type(self.__room_password) is list and len(self.__room_password) > 0:
            return self.__room_password[0]
        elif type(self.__room_password) is list:
            return None
        return self.__room_password
    
    @property
    def roons(self):
        return self.__roons
    
    def user_has_room(self):
        try:
            if self.user_room_id:
                query = "SELECT EXISTS (SELECT * FROM user_room WHERE user_room_id = %s and room_id = %s and user_id = %s)"
                parameters = (self.user_room_id, self.room_id, self.__user_id)
                db = Db()
                db.sync_connection_db()
                if db.sync_exists(query=query, parameters=parameters):
                    return True
            abort(403, "Acesso Negado..")
        except Exception as e:
            print(e)
            abort(500)
        
    def exists_user_room(self):
        try:
            if self.__user_id:   
                query = "SELECT EXISTS (SELECT user_room_id FROM user_room WHERE user_id = %s and room_id = %s);"
                parameters = (self.__user_id, self.room_id,)
                db = Db()
                db.sync_connection_db()
                if db.sync_exists(query=query, parameters=parameters):
                    self.__error = 'você já está nessa sala!'
                    return True
            return False
        except Exception as e:
            print(e)
            abort(500)
            
    def exists_room_name(self):
        try:
            if self.__user_id:   
                query = "SELECT EXISTS (SELECT room_id FROM room WHERE room_name = %s);"
                parameters = (self.room_name,)
                db = Db()
                db.sync_connection_db()
                result = db.sync_exists(query=query, parameters=parameters)
                if result:
                    self.__error = 'Esse nome de sala já existe!'
                    return True
            return False
        except Exception as e:
            print(e)
            abort(500)
            
    def exists_room(self):
        try:
            if self.room_id:   
                query = "SELECT EXISTS (SELECT * FROM room WHERE room_id = %s);"
                parameters = (self.room_id,)
                db = Db()
                db.sync_connection_db()
                if db.sync_exists(query=query, parameters=parameters):
                    return True
            abort(403, "Sala não existe!")
        except Exception as e:
            print(e)
            abort(500)
        
    def load_user_room(self):
        try:
            if self.__user_id: 
                query = """SELECT rm.room_id, rm.room_name, ur.user_room_id, ur.user_room_type 
                FROM user_room ur, room rm 
                WHERE ur.user_id = %s AND ur.room_id = rm.room_id;"""
                parameters = (self.__user_id,)
                db = Db()
                db.sync_connection_db()
                result = db.sync_select(query=query, parameters=parameters)
                if result:
                    for row in result:
                        self.__roons.append({
                            'room_id': row[0],
                            'room_name': row[1],
                            'user_room_id': row[2],
                            'can_delete': row[3] == 1
                        })
                return True
            return False
        except Exception as e:
            print(e)
            abort(500)
            
    def load_room(self):
        try:
            if self.room_id: 
                query = "SELECT room_name, room_password, room_image FROM room WHERE room_id = %s;"
                parameters = (self.room_id,)
                db = Db()
                db.sync_connection_db()
                result = db.sync_select(query=query, parameters=parameters, all=False)
                if result:
                    self.__room_name.append(result[0])
                    self.__room_password.append(result[1])
                    self.__background_cartesian_plane = result[2]
                return True
            return False
        except Exception as e:
            print(e)
            abort(500)
            
    def load_room_image(self):
        try:
            if self.room_id: 
                query = "SELECT room_image FROM room WHERE room_id = %s;"
                parameters = (self.room_id,)
                db = Db()
                db.sync_connection_db()
                result = db.sync_select(query=query, parameters=parameters, all=False)
                if result and result[0] is not None:
                    return True, result[0]
                return False, None
            return False, None
        except Exception as e:
            print(e)
            abort(500)
            
    def load_room_id(self):
        try:
            if self.room_name: 
                query = "SELECT room_id FROM room WHERE room_name = %s;"
                parameters = (self.room_name,)
                db = Db()
                db.sync_connection_db()
                result = db.sync_select(query=query, parameters=parameters, all=False)
                if result:
                    self.__room_id.append(result[0])
                    return True
                return False
            return False
        except Exception as e:
            print(e)
            abort(500)
                                                                                                                                                                                                                                                                                                          
    def insert_user_room(self, user_room_type=2):
        try:
            if self.__user_id and self.exists_user_room() is False:    
                query = """INSERT INTO user_room
                    (user_id, room_id, user_room_type) 
                    VALUES(%s,%s,%s) RETURNING user_room_id;"""
                parameters = (self.__user_id, self.room_id, user_room_type)
                db = Db()
                db.sync_connection_db()
                self.__user_room_id.append(db.sync_insert(query=query, parameters=parameters)) 
                self.__can_delete = user_room_type == 1
                return True
            return False
        except Exception as e:
            print(e)
            abort(500, 'Error INSERT!')
    
    def valid_password_room(self):
        try:
            if self.room_name:
                query = "SELECT EXISTS (SELECT room_id FROM room WHERE room_name = %s "
                query += "AND room_password = %s);" if self.room_password is not None else  "AND room_password IS NULL);"
                parameters = (self.room_name, self.room_password,) if self.room_password is not None else (self.room_name,)
                db = Db()
                db.sync_connection_db()
                if db.sync_exists(query=query, parameters=parameters):
                    return True
            self.__error = 'Senha ou Nome errado!'
            return False
        except Exception as e:
            print(e)
            abort(500, 'Error INSERT!')
            
    def insert_user_room_with_password(self):
        try:
            self.load_room_id()
            if self.__user_id and  self.exists_user_room() is False and self.valid_password_room():
                query = """
                INSERT INTO user_room
                (user_id, room_id) 
                VALUES(%s,%s) RETURNING user_room_id;
                """
                parameters = (self.__user_id, self.room_id)
                db = Db()
                db.sync_connection_db()
                self.__user_room_id.append(db.sync_insert(query=query, parameters=parameters))
                return True
            return False  
        except Exception as e:
            print(e)
            abort(500, 'Error INSERT!')
            return False  
        
    def insert_room(self):
        try:
            if self.exists_room_name():
                return False
            query = 'INSERT INTO room(room_name, room_password) VALUES(%s,%s) RETURNING room_id;' if self.room_password is not None else 'INSERT INTO room(room_name) VALUES(%s) RETURNING room_id;'
            parameters = (self.room_name, self.room_password) if self.room_password is not None else (self.room_name,)
            db = Db()
            db.sync_connection_db()
            self.__room_id.append(db.sync_insert(query=query, parameters=parameters))
            return self.insert_user_room(1)
        except Exception as e:
            print(e)
            abort(500, 'Error INSERT!')
            
    def update_room_image(self):
        try:
            if self.room_id: 
                image = self.background_cartesian_plane   
                img = Image()
                result_old, old_img = self.load_room_image()
                if result_old:
                    img.name = old_img
                    img.remove_file()
                query = """UPDATE room SET room_image = %s WHERE room_id = %s;"""
                parameters = (image, self.room_id)
                db = Db()
                db.sync_connection_db()
                img = Image(name=image)
                update_result = db.sync_update(query=query, parameters=parameters)
                return update_result, img.url_img if update_result else None
            return False, None
        except Exception as e:
            print(e)
            abort(500, 'Error UPDATE!')
            
    def can_delete_room(self):
        try:
            if self.room_id and self.__user_id:   
                query = "SELECT EXISTS (SELECT room_id FROM user_room WHERE room_id = %s and user_id = %s and user_room_type=1);"
                parameters = (self.room_id, self.__user_id,)
                db = Db()
                db.sync_connection_db()
                if db.sync_exists(query=query, parameters=parameters):
                    self.__can_delete = True
                    return True
            self.__error = 'Você não tem permissão para deletar essa sala!'
            self.__can_delete = False
            return False
        except Exception as e:
            print(e)
            abort(500)
            
    def delete_room(self):
        try: 
            if self.room_id and self.can_delete_room():  
                result_image, image = self.load_room_image()
                query = "DELETE FROM room WHERE room_id = %s;"
                parameters = (self.room_id,)
                db = Db()
                db.sync_connection_db()
                result = db.sync_delete(query=query, parameters=parameters)
                if result and result_image:
                    img = Image(name=image)  
                    return img.remove_file()
                return result
            return False
        except Exception as e:
            print(e)
            abort(500, 'Error DELETE!')
    
    def update_room_name(self):
        try:    
            if self.room_id:
                query = "UPDATE room SET room_name = %s WHERE room_id = %s"
                parameters = (self.room_name,self.room_id,)
                db = Db()
                db.sync_connection_db()
                return db.sync_update(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            abort(500, 'Error UPDATE!')
            
    def delete_user_room(self):
        try:
            if self.__user_id:    
                query = "DELETE FROM user_room WHERE room_id = %s and user_id = %s"
                parameters = (self.room_id, self.__user_id)
                db = Db()
                db.sync_connection_db()
                return db.sync_delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            abort(500, 'Error DELETE!')