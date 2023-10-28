from data import get_connection_without_async
import pymysql
from flask import abort
from datetime import datetime

class Messages:
    def __init__(self, id_room = None, offset = None, limit = None):
        self.__id_room = id_room
        self.__offset = offset or 0
        self.__limit = limit or 20
        self.__id_message = []
        self.__names = []
        self.__messages = []
        self.__times = []
        
    @property
    def messages(self):
        messages = {
            'offset': self.__offset,
            'limit': self.__limit,
            'messages': []
        }
        for id_message, name_character, time, message in zip(self.__id_message, self.__names, self.__times, self.__messages):
            messages['messages'].append({
                'id_message': id_message,
                'time': time,
                'name': name_character,
                'message': message
            })
        messages['messages'].reverse()
        return messages
                                
    def load_messages(self):
        try:
            with get_connection_without_async() as conn:
                with conn.cursor() as mycursor:    
                    query = """
                    SELECT mg.id_message, pr.nome_personagem, mg.time, mg.message FROM message mg, personagem pr WHERE mg.id_room = %s AND mg.id_personagem = pr.id_personagem ORDER BY mg.time DESC, mg.id_message DESC LIMIT %s OFFSET %s;
                    """
                    mycursor.execute(query, (self.__id_room, self.__limit, self.__offset,))
                    result = mycursor.fetchall()
                    if result:
                        for row in result:
                            self.__id_message.append(row[0])
                            self.__names.append(row[1])
                            self.__times.append(row[2].strftime('%d-%m-%Y %H:%M'))
                            self.__messages.append(row[3])
                        self.__offset += len(result)
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            abort(500, 'Erro no carregamento das mensagens')  