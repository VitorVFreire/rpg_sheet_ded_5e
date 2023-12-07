from flask import abort
from datetime import datetime
from src import Db

class Messages:
    def __init__(self, room_id = None, offset = None, limit = None):
        self.__room_id = room_id
        self.__offset = offset or 0
        self.__limit = limit or 50
        self.__messages = {
            'room_id': self.__room_id,
            'offset': self.__offset,
            'limit': self.__limit,
            'messages': []
        }
        
    @property
    def messages(self):
        return self.__messages
    
    async def load_messages(self):
        try:   
            if self.__room_id:
                query = """
                SELECT m.message_id, m.message, m.messagetime AS time, COALESCE(m.character_id, m.user_id) AS id, COALESCE(c.character_name, u.user_name) AS name
                FROM message m
                LEFT JOIN character c ON m.character_id = c.character_id
                LEFT JOIN "user" u ON m.user_id = u.user_id
                WHERE m.room_id = %s
				ORDER BY m.messagetime DESC, m.message_id DESC LIMIT %s OFFSET %s;
                """
                parameters = (self.__room_id, self.__limit, self.__offset,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    messages = []
                    for row in result:
                        messages.append(
                            {
                                'message_id': row[0],
                                'message': row[1],
                                'time': row[2].strftime('%d-%m-%Y %H:%M'),
                                'id': row[3],
                                'name': row[4]
                            }
                        )
                    self.__messages['messages'].extend(list(reversed(messages)))
                    self.__offset += len(result)
                    self.__messages['offset'] = self.__offset
                    return True
            return False
        except Exception as e:
            print(e)
            abort(500, 'Erro no carregamento das mensagens')