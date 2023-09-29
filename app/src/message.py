from data import get_connection_without_async
import pymysql
import random
import datetime
import re

class Message:
    def __init__(self, id_message = None, room = None , message = None, name_character = None, id_personagem = None):
        self.__id_message = id_message
        self.__message = message
        self.__room = room
        self.__name_character = name_character
        self.__id_personagem = id_personagem
        self.__exists_command = self.__message.find('!r')
        self.__parts = []
        self.__amount_dices = []
        self.__amount_sides = []
        self.__results = []
        self.__result_total = 0
        self.__command = None
        self.__math_account = ""
        self.__message_treated = {}
        
        self.insert_message_bank()
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
            
            if self.__name_character is not None:
                self.__message_treated['name'] = self.__name_character
            
            if self.__exists_command != -1:
                self.__message_treated['dices'] = {}
                self.__message_treated['dices']['amount_dices'] = self.__amount_dices
                self.__message_treated['dices']['amount_sides'] = self.__amount_sides
                                
                self.__message_treated['dices']['results'] = self.__results[0]
                self.__message_treated['dices']['result_total'] = self.__result_total
                
                self.__message = f"ROLL: {self.__result_total} -- rolls: {self.__results[0]}"
                self.insert_message_bank()
                self.__message_treated['message'] = self.__message
                
            return self.__message_treated
        except EOFError as e:
            print(e)
            return False  
        
    def insert_message_bank(self):
        try:
            if self.__id_personagem:
                with get_connection_without_async() as conn:
                    with conn.cursor() as mycursor:    
                        query = """INSERT INTO message
                            (id_personagem, message, id_room, time) 
                            VALUES(%s,%s,%s,%s);"""
                        mycursor.execute(query, (self.__id_personagem, self.__message, self.__room, datetime.datetime.now()))
                        self.__id_message = mycursor.lastrowid  
                        conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False  