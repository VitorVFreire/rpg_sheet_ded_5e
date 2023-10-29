import unittest
from src import Character, Race, Room, Message, Messages
import asyncio

class MessageTest(unittest.TestCase):
    @classmethod
    async def setUp(cls): 
        cls.usuario_teste = Character(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        await cls.usuario_teste.insert_user()
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
        await cls.usuario_teste.insert_character(id_race=cls.raca_teste.id_race,character_name='nome personagem teste')
        
        cls.room = Room(id_user = cls.usuario_teste.id_user, room_name = 'test_room')
        cls.response_insert_room_bank = cls.room.insert_room()
        cls.character = Room(id_room = cls.room.id_room, id_character = cls.usuario_teste.id_character)
        cls.character.insert_character_room()
        
        cls.message = Message(id_character=cls.usuario_teste.id_character, message='teste text') 
        cls.message_roll = Message(id_character=cls.usuario_teste.id_character, message='!r 1d20')
        
        cls.messages = Messages(id_room=cls.room.id_room)
        cls.response_messages = cls.messages.load_messages()         
    
    @classmethod
    async def tearDown(cls):
        cls.room.delete_room()
        await cls.raca_teste.delete_race()
        await cls.usuario_teste.delete_user() 
        
    async def test_text_basic_message(self):
        self.assertEqual('teste text', self.message.message['message'])   
        
    async def test_text_roll_message(self):
        self.assertIsNotNone(self.message_roll.message['dices'])
        
    async def test_result_roll_1d20_dice(self):
        self.assertTrue(self.message_roll.message['result'] > 0 and self.message_roll.message['result'] <= 20)
        
    async def test_number_dices_message_roll_1(self):
        self.assertEqual(self.message_roll.message['dices']['amount_dices'], 1)
        
    async def test_number_sides_message_roll_20(self):
        self.assertEqual(self.message_roll.message['dices']['amount_sides'], 20)
    
    async def test_get_text_in_message_roll_rolls(self):
        self.assertIn('-- roll:', self.message_roll.message['message'])
    
    async def test_load_messages_bank_true(self):
        self.assertTrue(self.response_messages)
        
    async def test_len_messages_bigger_0(self):
        self.assertTrue(len(self.messages.messages) > 0)
    
    async def test_there_is_message_in_messages_true(self):
        self.assertIn(self.message.message['message'], self.messages.messages['messages']['message'])
    
    async def test_offset_messages_equal_2(self):
        self.assertEqual(self.messages.messages['offset'], 2)
    
    
if __name__ == '__main__':
    asyncio.run(unittest.main())