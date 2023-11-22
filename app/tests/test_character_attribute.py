import unittest
from src import CharacterAttribute, User, Race
import asyncio

class CharacterAttributeTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = User(name='John', email='john@example.com', password='pass123', birth_date='1990-01-01')
        await cls.usuario_teste.insert_user()
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
        cls.nome_personagem_teste = 'Personagem de Teste'

        cls.personagem_teste = CharacterAttribute(
            user_id=cls.usuario_teste.user_id,
            race_id=cls.raca_teste.race_id,
            nome_personagem=cls.nome_personagem_teste
        )
        await cls.personagem_teste.insert_character()
        
    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_character()
        await cls.usuario_teste.delete_user()
        await cls.raca_teste.delete_race()
        
    async def test_adiciona_atributo_forca_10_personagem(self):
        if await self.personagem_teste.exists_attributes():
            await self.personagem_teste.update_attributes(key='forca',value=10)
        else:
            await self.personagem_teste.insert_attribute(key='forca',value=10)
        await self.personagem_teste.load_attributes()
        self.assertEqual(self.personagem_teste.strength,10)
    
    async def test_existencia_atributos_espera_True(self):
        self.assertTrue(await self.personagem_teste.exists_attributes())
        
    async def test_bonus_forca_personagem_espera_0(self):
        await self.personagem_teste.load_attributes()
        self.assertEqual(self.personagem_teste.strength_bonus, 0)
        
    async def test_update_atributo_forca_16_personagem(self):
        if await self.personagem_teste.exists_attributes():
            await self.personagem_teste.update_attributes(key='forca',value=16)
            await self.personagem_teste.load_attributes()
            self.assertEqual(self.personagem_teste.strength,16)
            self.assertEqual(self.personagem_teste.strength_bonus, 3)
        
    async def test_adiciona_atributo_inteligencia_12_personagem(self):
        if await self.personagem_teste.exists_attributes():
            await self.personagem_teste.update_attributes(key='inteligencia',value=12)
        else:
            await self.personagem_teste.insert_attribute(key='inteligencia',value=12)
        await self.personagem_teste.load_attributes()
        self.assertEqual(self.personagem_teste.intelligence,12)
        
    async def test_bonus_inteligencia_personagem_espera_1(self):
        self.personagem_teste.load_attributes()
        self.assertEqual(self.personagem_teste.intelligence_bonus, 1)
        
    async def test_adiciona_atributo_bonus_proficiencia_2_personagem(self):
        if await self.personagem_teste.exists_attributes():
            await self.personagem_teste.update_attributes(key='bonus_proficiencia',value=2)
        else:
            await self.personagem_teste.insert_attribute(key='bonus_proficiencia',value=2)
        await self.personagem_teste.load_attributes()
        self.assertEqual(self.personagem_teste.proficiency_bonus,2)
        
if __name__ == '__main__':
    asyncio.run(unittest.main())