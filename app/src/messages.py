from flask import abort
from datetime import datetime
from src import Db

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
    
    async def load_messages(self):
        try:   
            if self.__room_id:
                query = """
                SELECT m.message_id, m.message, m.messagetime AS time, m.character_id, c.character_name, m.user_id, u.user_name
                FROM message m
                LEFT JOIN character c ON m.character_id = c.character_id
                LEFT JOIN "user" u ON m.user_id = u.user_id
                WHERE m.room_id = %s AND (m.character_id IS NOT NULL OR c.character_id IS NOT NULL) AND (m.user_id IS NOT NULL OR u.user_id IS NOT NULL)
                ORDER BY mg.time DESC, mg.message_id DESC LIMIT %s OFFSET %s;
                """
                parameters = (self.__room_id, self.__limit, self.__offset,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
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