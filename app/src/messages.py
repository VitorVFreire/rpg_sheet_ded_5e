from flask import abort
from datetime import datetime

class Messages:
    def __init__(self, room_id = None, offset = None, limit = None):
        self.__room_id = room_id
        self.__offset = offset or 0
        self.__limit = limit or 20
        self.__message_id = []
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
        for message_id, name_character, time, message in zip(self.__message_id, self.__names, self.__times, self.__messages):
            messages['messages'].append({
                'message_id': message_id,
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
                    SELECT mg.message_id, pr.character_name, mg.time, mg.message FROM message mg, personagem pr WHERE mg.room_id = %s AND mg.id_personagem = pr.id_personagem ORDER BY mg.time DESC, mg.message_id DESC LIMIT %s OFFSET %s;
                    """
                    mycursor.execute(query, (self.__room_id, self.__limit, self.__offset,))
                    result = mycursor.fetchall()
                    if result:
                        for row in result:
                            self.__message_id.append(row[0])
                            self.__names.append(row[1])
                            self.__times.append(row[2].strftime('%d-%m-%Y %H:%M'))
                            self.__messages.append(row[3])
                        self.__offset += len(result)
                        return True
            return False
        except Exception as e:
            print(e)
            abort(500, 'Erro no carregamento das mensagens')  