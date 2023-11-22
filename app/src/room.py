from data import get_connection_without_async
import pymysql
from flask import abort

class Room:
    def __init__(self, id_room=None, id_character=None, user_id=None, room_name=None, id_character_room=None):
        self.__id_room = id_room or []
        self.__name_room = room_name or []
        self._id_character = id_character
        self.__user_id = user_id
        self.__id_character_room = id_character_room
    
    @property    
    def roons(self):
        roons = []
        for id_room, name_room in zip(self.__id_room, self.__name_room):
            roons.append({'id_room': id_room, 'name_room': name_room})
        return roons      
    
    @property
    def id_room(self):
        return self.__id_room
    
    @property
    def name_room(self):
        return self.__name_room
        
    def exists_character_room(self):
        try:
            if self._id_character:
                with get_connection_without_async() as conn:
                    with conn.cursor() as mycursor:    
                        query = "SELECT EXISTS (SELECT id_room_personagem FROM room_personagem WHERE id_personagem = %s and id_room = %s)"
                        mycursor.execute(query, (self._id_character, self.__id_room,))
                        result = mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            abort(500)
        
    def character_belongs_room(self):
        try:
            if self._id_character:
                with get_connection_without_async() as conn:
                    with conn.cursor() as mycursor:    
                        query = "SELECT EXISTS (SELECT id_room_personagem FROM room_personagem WHERE id_personagem = %s and id_room = %s)"
                        mycursor.execute(query, (self._id_character, self.__id_room,))
                        result = mycursor.fetchone()
                        if result[0] == 1:
                            return True
            abort(403, "Acesso Negado")
        except pymysql.Error as e:
            print(e)
            abort(500)
        
    def load_character_room(self):
        try:
            if self._id_character:
                with get_connection_without_async() as conn:
                    with conn.cursor() as mycursor:    
                        query = "SELECT rm.id_room, rm.nome_room  FROM room_personagem rp, room rm WHERE rp.id_personagem = %s and rp.id_room = rm.id_room;"
                        mycursor.execute(query, (self._id_character,))
                        result = mycursor.fetchall()
                        if result:
                            for row in result:
                                self.__id_room.append(row[0])
                                self.__name_room.append(row[1])
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            abort(500)
                                                                                                                                                                                                                                                                                                          
    def insert_character_room(self):
        try:
            if self._id_character and self.exists_character_room() is False:
                with get_connection_without_async() as conn:
                    with conn.cursor() as mycursor:    
                        query = """INSERT INTO room_personagem
                            (id_personagem, id_room, permissao) 
                            VALUES(%s,%s,0);"""
                        mycursor.execute(query, (self._id_character, self.__id_room))
                        self.__id_character_room = mycursor.lastrowid  
                        conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            abort(500, 'Erro na inserção ao banco')
        
    def insert_room(self):
        try:
            if self.__user_id:
                with get_connection_without_async() as conn:
                    with conn.cursor() as mycursor:    
                        query = """INSERT INTO room
                            (id_usuario, nome_room) 
                            VALUES(%s,%s);"""
                        mycursor.execute(query, (self.__user_id, self.__name_room))
                        self.__id_room = mycursor.lastrowid  
                        conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            abort(500, 'Erro na inserção ao banco')
            
    def delete_room(self):
        try:
            with get_connection_without_async() as conn:
                with conn.cursor() as mycursor:    
                    query = """DELETE FROM room WHERE id_room = %s"""
                    mycursor.execute(query, (self.__id_room,))
                    conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            abort(500, 'Erro na exclusão da sala')
    
    def update_room(self):
        try:
            with get_connection_without_async() as conn:
                with conn.cursor() as mycursor:    
                    query = """UPDATE room SET nome_room = %s WHERE id_room = %s"""
                    mycursor.execute(query, (self.__name_room,self.__id_room,))
                    conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            abort(500, 'Erro na exclusão da sala')
            
    def delete_character_room(self):
        try:
            if self.__user_id:
                with get_connection_without_async() as conn:
                    with conn.cursor() as mycursor:    
                        query = """DELETE FROM room_personagem WHERE id_room = %s and id_personagem = %s"""
                        mycursor.execute(query, (self.__id_room, self._id_character))
                        conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            abort(500, 'Erro na exclusão da sala')