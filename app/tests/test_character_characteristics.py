import unittest
from src import CharacterCharacteristics, User, Race, Spell
import asyncio

class CharacterCharacteristicsTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = User(name='John', email='john@example.com', password='pass123', birth_date='1990-01-01')
        await cls.usuario_teste.insert_user()
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
        cls.nome_personagem_teste = 'Personagem de Teste'
        
        cls.personagem_teste = CharacterCharacteristics(
            user_id=cls.usuario_teste.user_id,
            race_id=cls.raca_teste.race_id,
            nome_personagem=cls.nome_personagem_teste,
        )
        cls.response_insert_personagem = await cls.personagem_teste.insert_character()  
        cls.response_insert_carct = await cls.personagem_teste.insert_characteristics(key='idade', value=10)   
        cls.response_load_caract = await cls.personagem_teste.load_characteristics()  
   
    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_character()
        await cls.usuario_teste.delete_user()
        await cls.raca_teste.delete_race()  
        
    async def test_exists_caracteristica_bank_false(self):
        self.assertFalse(self.personagem_teste.exists_characteristics()) 
        
    async def test_personagem_criado_true(self):
        self.assertTrue(self.response_insert_personagem)
        
    async def test_caracteristica_insert_bank_true(self):
        self.assertTrue(self.response_insert_carct)
       
    async def test_load_caracteristicas_personagem_true(self):
        self.assertTrue(self.response_load_caract)
        
    async def test_idade_10(self):
        self.assertEqual(self.personagem_teste.age, 10)
        
    async def test_update_idade_20(self):
        self.assertTrue(self.personagem_teste.update_characteristics(key='idade', value=20))
        self.assertTrue(self.personagem_teste.load_characteristics())
        self.assertEqual(self.personagem_teste.age, 20)
        self.assertNotEqual(self.personagem_teste, 10)
        
    async def test_update_cor_olhos_vermelho_true(self):
        self.assertTrue(self.personagem_teste.update_characteristics(key='cor_olhos', value='vermelho'))
        self.assertEqual(self.personagem_teste.eye_color, 'vermelho')
        
    async def test_cor_pele_is_none(self):
        self.assertIsNone(self.personagem_teste.skin_color)
        
    async def test_delete_caracterisca_bank_true(self):
        self.assertTrue(self.personagem_teste.delete_characteristics())
                    
if __name__ == '__main__':
    asyncio.run(unittest.main())