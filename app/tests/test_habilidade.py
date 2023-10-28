import unittest
import asyncio
from src import Spell
import requests

class HabilidadeTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
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
            spell_name = 'teste_habilidade 2',
            sides_dices = 323,
            link_details = 'https://aventureirosdosreinos.com/bola-de-fogo/',
            damege_type = 'agua',
            amount_dices = 323,
            level_spell = 3,
            additional_per_level = 3 
        ) 
        
        await cls.habilidade_teste_2.insert_spell()
        
    @classmethod
    async def tearDown(cls):
        await cls.habilidade_teste.delete_spell() 
        await cls.habilidade_teste_2.delete_spell() 
        
    async def test_insert_sucess_true(self):
        self.assertTrue(self.response_insert)
        
    async def test_nome_atributo_inteligencia_true(self):
        self.assertEqual(self.habilidade_teste.attribute_name, 'inteligencia')
    
    async def test_out_link_code_200(self):
        self.assertEqual(requests.get(url=self.habilidade_teste.link_details).status_code, 200)
    
    async def test_get_text_link_detalhes_true(self):
        self.assertIn(self.habilidade_teste.damege_type, requests.get(url=self.habilidade_teste.link_details).encoding)

    async def test_habilidade_is_dic(self):
        self.assertIs(self.habilidade_teste.spell, dict())
        
    async def test_len_habilidades_bigger_equal_2(self):
        habilidades = Spell()
        habilidades.load_spells()
        self.assertTrue(len(habilidades.spells) >= 2)
        
    async def test_habilidade_name_in_habilidades(self):
        habilidades = Spell()
        habilidades.load_spells()
        self.assertIn(self.habilidade_teste.attribute_name, habilidades.spells)
        
    async def test_habilidade_nome_atributo_equal_load_for_id_habilidade(self):
        habilidades = Spell(id_spell = self.habilidade_teste.id_spell)
        habilidades.load_spell()
        self.assertEqual(self.habilidade_teste.attribute_name, habilidades.attribute_name)

if __name__ == '__main__':
    asyncio.run(unittest.main())