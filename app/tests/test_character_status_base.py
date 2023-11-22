import unittest
from src import CharacterStatusBase, User, Race
import asyncio

class CharacterStatusBaseTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = User(name='John', email='john@example.com', password='pass123', birth_date='1990-01-01')
        await cls.usuario_teste.insert_user()
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
        cls.nome_personagem_teste = 'Personagem de Teste'

        cls.personagem_teste = CharacterStatusBase(
            user_id=cls.usuario_teste.user_id,
            id_raca=cls.raca_teste.race_id,
            nome_personagem=cls.nome_personagem_teste
        )
        await cls.personagem_teste.insert_character()

    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_character()
        await cls.usuario_teste.delete_user()
        await cls.raca_teste.delete_race()
    
    async def test_validar_existencia_status_base_false(self):
        self.assertFalse(await self.personagem_teste.exists_status_base())

    async def test_adicionar_status_base_vida_20(self):
        self.assertTrue(await self.personagem_teste.insert_status_base(key='vida', value=20))

    async def test_validar_existencia_vida_personagem_true(self):
        self.assertTrue(await self.personagem_teste.exists_status_base())
        
    async def test_vida_personagem_equal_20(self):
        self.assertEqual(await self.personagem_teste.hit_points, 20)
        
    async def test_update_vida_personagem_true(self):
        self.assertTrue(await self.personagem_teste.update_status_base(key='vida', value=10))
    
    async def test_vida_personagem_equal_10(self):
        self.assertEqual(await self.personagem_teste.hit_points, 10)
        
    async def test_load_status_base_true_vida_10_nivel_none(self):
        status_base = CharacterStatusBase(id_character = self.personagem_teste.id_character, user_id = self.usuario_teste.user_id)
        self.assertTrue(await status_base.load_status_base())
        self.assertEqual(status_base.hit_points, 10)
        self.assertIsNone(status_base.level)
    
    async def test_adicionar_status_base_xp_20(self):
        self.assertTrue(await self.personagem_teste.insert_status_base(key='xp', value=20))
    
    async def test_load_status_base_true_vida_10_xp_20(self):
        status_base = CharacterStatusBase(id_character = self.personagem_teste.id_character, user_id = self.usuario_teste.user_id)
        self.assertTrue(await status_base.load_status_base())
        self.assertEqual(status_base.hit_points, 10)
        self.assertEqual(status_base.experience_points, 10)
         
    async def test_delete_vida_personagem_true(self):
        self.assertTrue(await self.personagem_teste.delete_character_class())

if __name__ == '__main__':
    asyncio.run(unittest.main())