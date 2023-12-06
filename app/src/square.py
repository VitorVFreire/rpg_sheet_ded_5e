from flask import abort
from src import Db, Image
import random

class Square:
    def __init__(self, square_id=None, user_room_id=None, x=None, y=None, square_image=None, room_id=None):
        self.__square_id = square_id or []
        self.__room_id = room_id
        self.__user_room_id = user_room_id or []
        self.__x = x or []
        self.__y = y or []
        self.__square_image = square_image or []
    
    @property    
    def squares(self):
        if self.square_id:
            squares = []
            for square_id, x, y, square_image in zip(self.square_id, self.__x, self.__y, self.square_image):
                squares.append({'square_id': square_id, 'x': x, 'y': y, 'square_image': square_image})
            return squares if len(squares) > 0 else None   
        return None 
    
    @property
    def square_id(self):
        return self.__square_id
    
    @property
    def square_image(self):
        img = Image(parameters='square')
        if type(self.__square_image) is not list and self.__square_image is not None:
            result, name = img.save_file(self.__square_image)
            return name
        elif type(self.__square_image) is list and len(self.__square_image) > 0:
            return self.__square_image
        img.name = img.img_default_path(index=1)
        return [img.url_img]
                  
    def load_squares(self):
        try:
            if self.__room_id: 
                query = """SELECT sq.square_id, sq.x, sq.y, sq.square_image 
                FROM square sq
                JOIN user_room ur ON ur.user_room_id = sq.user_room_id
                WHERE ur.room_id = %s
                ;"""
                parameters = (self.__room_id,)
                db = Db()
                db.sync_connection_db()
                result = db.sync_select(query=query, parameters=parameters)
                if result:
                    for row in result:
                        self.__square_id.append(row[0])
                        self.__x.append(row[1])
                        self.__y.append(row[2])
                        self.__square_image.append(row[3])
                return True
            return False
        except Exception as e:
            print(e)
            abort(500)
                                                                                                                                                                                                                                                                                                          
    def insert_square(self):
        try:
            if self.__user_room_id:    
                x = random.randint(0, 5)
                y = random.randint(0, 5)
                query = """INSERT INTO square
                    (user_room_id, x, y, square_image) 
                    VALUES(%s,%s,%s,%s) RETURNING square_id;"""
                parameters = (self.__user_room_id, x, y, self.square_image[0])
                db = Db()
                db.sync_connection_db()
                self.__square_id.append(db.sync_insert(query=query, parameters=parameters))
                self.__x.append(x)
                self.__y.append(y)
                return True
            return False
        except Exception as e:
            print(e)
            abort(500, 'Erro na inserção ao banco')
                   
    def delete_square(self):
        try:    
            query = "DELETE FROM square WHERE square_id = %s"
            parameters = (self.__square_id,)
            db = Db()
            db.sync_connection_db()
            return db.sync_delete(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            abort(500, 'Erro na exclusão da square')
    
    def update_square_position(self):
        try:    
            query = "UPDATE square SET x = %s, y = %s WHERE square_id = %s"
            parameters = (self.__x, self.__y, self.__square_id,)
            db = Db()
            db.sync_connection_db()
            return db.sync_update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            abort(500, 'Erro na update da square')
            
    def update_square_image(self):
        try:    
            query = "UPDATE square SET square_image = %s WHERE square_id = %s"
            parameters = (self.square_image, self.__square_id,)
            db = Db()
            db.sync_connection_db()
            return db.sync_update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            abort(500, 'Erro na update da square da imagem')
            
    def delete_square(self):
        try:
            if self.square_id:    
                query = "DELETE FROM square WHERE square_id = %s"
                parameters = (self.__square_id)
                db = Db()
                db.sync_connection_db()
                return db.sync_delete(query=query, parameters=parameters)
            return False
        except Exception as e:
            print(e)
            abort(500, 'Erro na exclusão da square')