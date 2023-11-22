import unittest
from src import CharacterSpell, User, Race, Spell
import asyncio

class CharacterSpellTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = User(name='John', email='john@example.com', password='pass123', birth_date='1990-01-01')
        await cls.usuario_teste.insert_user()
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
        cls.nome_personagem_teste = 'Personagem de Teste'
        
        cls.habilidade_teste = Spell(
            attribute_name = 'inteligencia',
            spell_name = 'teste_habilidade',
            sides_dices = 20,
            link_details = 'https://aventureirosdosreinos.com/bola-de-fogo/',
            damege_type = 'fogo',
            amount_dices = 5,
            level_spell = 3,
            additional_per_level = 3 
        )
        cls.response_insert = await cls.habilidade_teste.insert_spell() 

        cls.habilidade_teste_2 = Spell(
            attribute_name = 'inteligencia',
            spell_name = 'teste_habilidade_2',
            sides_dices = 20,
            link_details = 'https://aventureirosdosreinos.com/bola-de-fogo/',
            damege_type = 'fogo',
            amount_dices = 5,
            level_spell = 3,
            additional_per_level = 3 
        )
        await cls.habilidade_teste_2.insert_spell() 

        
        cls.personagem_teste = CharacterSpell(
            user_id=cls.usuario_teste.user_id,
            race_id=cls.raca_teste.race_id,
            nome_personagem=cls.nome_personagem_teste,
        )
        await cls.personagem_teste.insert_character()
        
        cls.response_insert_habilidade = await cls.personagem_teste.insert_spell(cls.habilidade_teste.spell_id)
        cls.response_load_habilidade_personagem = await cls.personagem_teste.load_spells()
        
    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_character()
        await cls.usuario_teste.delete_user()
        await cls.habilidade_teste.delete_spell()
        await cls.habilidade_teste_2.delete_spell()
        await cls.raca_teste.delete_race()    
        
    async def test_load_habilidades_true(self):
        self.assertTrue(self.response_load_habilidade_personagem)
       
    async def test_insert_habilidade_personagem_true(self):
        self.assertTrue(self.response_insert_habilidade)
        
    async def test_name_habilidade_equal_name_habilidade_personagem_teste_habilidade(self):
        self.assertEqual(self.habilidade_teste.spell_name, self.personagem_teste.spells[0]['nome_habilidade'])   
        
    async def test_update_habilidade_personagem(self):
        self.assertTrue(self.personagem_teste.update_spell(spell_id=self.habilidade_teste_2.spell_id, character_id_spell=self.personagem_teste.spell[0]['id_habilidade_personagem']))
        self.assertTrue(self.personagem_teste.load_spells())
        self.assertEqual(self.personagem_teste.spell[0]['nome_habilidade'], self.habilidade_teste_2.spell_name)
        
    async def test_habilidade1_dif_habilidade2(self):
        self.assertNotEqual(self.habilidade_teste.spell_name, self.habilidade_teste_2.spell_name)

    async def test_adiconar_habilidade_personagem_habilidades_bigger_equal_2(self):
        self.assertTrue(self.personagem_teste.insert_spell(spell_id=self.habilidade_teste.spell_id))
        self.assertTrue(self.personagem_teste.load_spells())
        self.assertTrue(len(self.personagem_teste.spells) > 0)
    
if __name__ == '__main__':
    asyncio.run(unittest.main())