import unittest
from src import Character, Race, Room
import asyncio

class RoomTest(unittest.TestCase):
    @classmethod
    async def setUp(cls): 
        cls.usuario_teste = Character(nome='John', email='john@example.com', password='pass123', birth_date='1990-01-01')
        await cls.usuario_teste.insert_user()
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
        await cls.usuario_teste.insert_character(race_id=cls.raca_teste.race_id,character_name='nome personagem teste')
        
        cls.room = Room(user_id = cls.usuario_teste.user_id, room_name = 'test_room')
        cls.response_insert_room_bank = cls.room.insert_room()
        cls.character = Room(id_room = cls.room.id_room, id_character = cls.usuario_teste.id_character)
        cls.character.insert_character_room()   
    
    @classmethod
    async def tearDown(cls):
        cls.room.delete_room()
        await cls.raca_teste.delete_race()
        await cls.usuario_teste.delete_user()
    
    async def test_create_room_bank_true(self):
        self.assertTrue(self.response_insert_room_bank)
    
    async def test_exists_character_bank_true(self):
        self.assertTrue(self.character.exists_character_room())
    
    async def test_belongs_character_room_true(self):
        self.assertTrue(self.character.character_belongs_room())
        
    async def test_load_roons_len_bigger_0(self):
        roons = Room(id_character=self.usuario_teste.id_character)
        roons.load_character_room()
        self.assertTrue(len(roons.roons) > 0)
        
    async def test_update_name_room_true(self):
        room = Room(id_room = self.room.id_room, room_name='new teste name room')
        self.assertTrue(room.update_room())
        self.assertNotEqual(room.name_room, self.room.name_room)
        self.assertEqual(room.id_room, self.room.id_room)
        
    async def test_delete_character_room_bank_true(self):
        self.assertTrue(self.character.delete_character_room())
        
    async def test_load_roons_len_equal_0(self):
        roons = Room(id_character=self.usuario_teste.id_character)
        roons.load_character_room()
        self.assertEqual(len(roons.roons), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())