import unittest
import asyncio
from src import Habilidade
import requests

class HabilidadeTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.habilidade_teste = Habilidade(
            nome_atributo = 'inteligencia',
            nome_habilidade = 'teste_habilidade',
            lados_dados = 20,
            link_detalhes = 'https://aventureirosdosreinos.com/bola-de-fogo/',
            tipo_dano = 'fogo',
            qtd_dados = 5,
            nivel_habilidade = 3,
            adicional_por_nivel = 3 
        )
        cls.response_insert = await cls.habilidade_teste.insert_habilidade_banco() 
        
        cls.habilidade_teste_2 = Habilidade(
            nome_atributo = 'inteligencia',
            nome_habilidade = 'teste_habilidade 2',
            lados_dados = 323,
            link_detalhes = 'https://aventureirosdosreinos.com/bola-de-fogo/',
            tipo_dano = 'agua',
            qtd_dados = 323,
            nivel_habilidade = 3,
            adicional_por_nivel = 3 
        ) 
        
        await cls.habilidade_teste_2.insert_habilidade_banco()
        
    @classmethod
    async def tearDown(cls):
        await cls.habilidade_teste.delete_habilidade_banco() 
        await cls.habilidade_teste_2.delete_habilidade_banco() 
        
    async def test_insert_sucess_true(self):
        self.assertTrue(self.response_insert)
        
    async def test_nome_atributo_inteligencia_true(self):
        self.assertEqual(self.habilidade_teste.nome_atributo, 'inteligencia')
    
    async def test_out_link_code_200(self):
        self.assertEqual(requests.get(url=self.habilidade_teste.link_detalhes).status_code, 200)
    
    async def test_get_text_link_detalhes_true(self):
        self.assertIn(self.habilidade_teste.tipo_dano, requests.get(url=self.habilidade_teste.link_detalhes).encoding)

    async def test_habilidade_is_dic(self):
        self.assertIs(self.habilidade_teste.habilidade, dict())
        
    async def test_len_habilidades_bigger_equal_2(self):
        habilidades = Habilidade()
        habilidades.carregar_habilidades()
        self.assertTrue(len(habilidades.habilidades) >= 2)
        
    async def test_habilidade_name_in_habilidades(self):
        habilidades = Habilidade()
        habilidades.carregar_habilidades()
        self.assertIn(self.habilidade_teste.nome_atributo, habilidades.habilidades)
        
    async def test_habilidade_nome_atributo_equal_load_for_id_habilidade(self):
        habilidades = Habilidade(id_habilidade = self.habilidade_teste.id_habilidade)
        habilidades.carregar_habilidade()
        self.assertEqual(self.habilidade_teste.nome_atributo, habilidades.nome_atributo)

if __name__ == '__main__':
    asyncio.run(unittest.main())