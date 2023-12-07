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
            square_imgs = []
            for square_img in self.__square_image:
                img.name = square_img
                square_imgs.append(img.url_img)
            return square_imgs
        img.name = img.img_default_path(index=1)
        return [img.name]
                  
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
            
    def load_square_image(self):
        try:
            if self.__square_id: 
                query = "SELECT square_image FROM square WHERE square_id = %s;"
                parameters = (self.__square_id,)
                db = Db()
                db.sync_connection_db()
                result = db.sync_select(query=query, parameters=parameters, all=False)
                if result:
                    if type(self.__square_image) is not list:
                        self.__square_image = result[0]
                    else:
                        self.__square_image.append(result[0])
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
                img  = Image()
                img.name = img.img_default_path(index=1)
                return True, {'square_id': db.sync_insert(query=query, parameters=parameters), 'x': x, 'y': y, 'square_image': img.url_img}
            return False
        except Exception as e:
            print(e)
            abort(500, 'Erro na inserção ao banco')
                   
    def delete_square(self):
        try:    
            self.load_square_image()          
            query = "DELETE FROM square WHERE square_id = %s;"
            parameters = (self.__square_id,)
            db = Db()
            db.sync_connection_db()
            result = db.sync_delete(query=query, parameters=parameters)
            if result and self.__square_image[0]:
                img = Image(name=self.__square_image[0])  
                return img.remove_file()
            return result
        except Exception as e:
            print(e)
            abort(500, 'Erro na exclusão da square')
    
    def update_square_position(self):
        try:    
            x = self.__x if type(self.__x) is not list else 0
            y = self.__y if type(self.__y) is not list else 0
            query = "UPDATE square SET x = %s, y = %s WHERE square_id = %s"
            parameters = (x, y, self.__square_id,)
            db = Db()
            db.sync_connection_db()
            return db.sync_update(query=query, parameters=parameters)
        except Exception as e:
            print(e)
            abort(500, 'Erro na update da square')
            
    def update_square_image(self):
        try:    
            image = self.square_image
            img = Image()
            if self.load_square_image() and self.__square_image is not None:
                img.name = self.__square_image
                img.remove_file()
            query = "UPDATE square SET square_image = %s WHERE square_id = %s"
            parameters = (image, self.__square_id,)
            db = Db()
            db.sync_connection_db()
            img.name = image
            return db.sync_update(query=query, parameters=parameters), img.url_img
        except Exception as e:
            print(e)
            abort(500, 'Erro na update da square da imagem')
            