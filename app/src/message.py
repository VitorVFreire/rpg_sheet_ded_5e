import random
import datetime
import re
from src import Db

class Message:
    def __init__(self, message_id = None, room_id = None , message = None, name = None, character_id = None, user_id=None):
        self.__message_id = message_id
        self.__message = message
        self.__room_id = room_id
        self.__name = name
        self.__character_id = character_id
        self.__user_id = user_id
        self.__exists_command = self.__message.find('!r')
        self.__parts = []
        self.__amount_dices = []
        self.__amount_sides = []
        self.__results = []
        self.__result_total = 0
        self.__command = None
        self.__math_account = ""
        self.__message_treated = {}
        
        self.insert_message()
        if self.__exists_command != -1:
            self.filtering_message()
            
    def roll_dice(self):
        results = []
        for dice in range(self.__amount_dices[-1]):
            results.append(int(random.randint(1, self.__amount_sides[-1])))
        self.__results.append(results)
        self.__math_account += f'{sum(results)} '
                    
    def filtering_message(self):
        try:
            self.__command = self.__message[self.__exists_command + 3:]
            self.__parts = self.__command.split(' ')
            for part in self.__parts:
                location_d = part.find('d')
                bonus = re.search(r"[-+*/]\s*\d+", part)
                if location_d != -1:
                    self.__amount_dices.append(int(part[:location_d]))
                    self.__amount_sides.append(int(part[location_d + 1:]))
                    self.roll_dice()
                elif part in ['+', '-', '*', '/']:
                    self.__math_account += f'{part} '
                elif bonus is not None:
                    self.__math_account += f'{bonus.group(0)} '
            self.__result_total = eval(self.__math_account)
        except:
            self.__message = 'Erro na rolagem dos dados!'
            self.__exists_command = -1
            
    @property
    def message(self):
        try:
            self.__message_treated['message'] = self.__message
                
            self.__message_treated['time'] = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')       
            
            if self.__name is not None:
                self.__message_treated['name'] = self.__name
            
            if self.__exists_command != -1:
                self.__message_treated['dices'] = {}
                self.__message_treated['dices']['amount_dices'] = self.__amount_dices
                self.__message_treated['dices']['amount_sides'] = self.__amount_sides
                                
                self.__message_treated['dices']['results'] = self.__results[0]
                self.__message_treated['dices']['result_total'] = self.__result_total
                
                self.__message = f"ROLL: {self.__result_total} -- rolls: {self.__results[0]}"
                self.insert_message()
                self.__message_treated['message'] = self.__message
                
            return self.__message_treated
        except EOFError as e:
            print(e)
            return False  
        
    def insert_message(self):
        try:
            if self.__room_id:    
                query = """
                INSERT INTO message
                (room_id, character_id, user_id, messagetime, message) 
                VALUES(%s,%s,%s,%s,%s) RETURNING message_id;
                """
                parameters = (self.__room_id, self.__character_id, self.__user_id, datetime.datetime.now(), self.__message)
                db = Db()
                db.sync_connection_db()
                self.__message_id = db.sync_insert(query=query, parameters=parameters)  
                return True
            return False
        except Exception as e:
            print(e)
            return False  