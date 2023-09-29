import unittest
from src import Personagem, Raca, Room
import asyncio

class TestRoom(unittest.TestCase):
    @classmethod
    async def setUp(cls): 
        cls.usuario_teste = Personagem(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        await cls.usuario_teste.create_usuario()
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        await cls.raca_teste.insert_raca_banco()
        await cls.usuario_teste.adicionar_personagem_banco(id_raca=cls.raca_teste.id_raca,nome_personagem='nome personagem teste')
        
        cls.room = Room(id_usuario = cls.usuario_teste.id, name_room = 'test_room')
        cls.response_insert_room_bank = cls.room.insert_room_bank()
        cls.character = Room(id_room = cls.room.id_room, id_personagem = cls.usuario_teste.id_personagem)
        cls.character.insert_character_room_bank()   
    
    @classmethod
    async def tearDown(cls):
        cls.room.delete_room_bank()
        await cls.raca_teste.delete_raca_banco()
        await cls.usuario_teste.delete_usuario()
    
    async def test_create_room_bank_true(self):
        self.assertTrue(self.response_insert_room_bank)
    
    async def test_exists_character_bank_true(self):
        self.assertTrue(self.character.exists_character_room_bank())
    
    async def test_belongs_character_room_true(self):
        self.assertTrue(self.character.character_belongs_room())
        
    async def test_load_roons_len_bigger_0(self):
        roons = Room(id_personagem=self.usuario_teste.id_personagem)
        roons.load_character_room()
        self.assertTrue(len(roons.roons) > 0)
        
    async def test_update_name_room_true(self):
        room = Room(id_room = self.room.id_room, name_room='new teste name room')
        self.assertTrue(room.update_room_bank())
        self.assertNotEqual(room.name_room, self.room.name_room)
        self.assertEqual(room.id_room, self.room.id_room)
        
    async def test_delete_character_room_bank_true(self):
        self.assertTrue(self.character.delete_character_room_bank())
        
    async def test_load_roons_len_equal_0(self):
        roons = Room(id_personagem=self.usuario_teste.id_personagem)
        roons.load_character_room()
        self.assertEqual(len(roons.roons), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())