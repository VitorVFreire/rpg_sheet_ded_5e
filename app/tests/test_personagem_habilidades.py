import unittest
from src import PersonagemHabilidades, Usuario, Raca, Habilidade
import asyncio

class PersonagemHabilidadesTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = Usuario(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        await cls.usuario_teste.create_usuario()
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        await cls.raca_teste.insert_raca_banco()
        cls.nome_personagem_teste = 'Personagem de Teste'
        
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
            nome_habilidade = 'teste_habilidade_2',
            lados_dados = 20,
            link_detalhes = 'https://aventureirosdosreinos.com/bola-de-fogo/',
            tipo_dano = 'fogo',
            qtd_dados = 5,
            nivel_habilidade = 3,
            adicional_por_nivel = 3 
        )
        await cls.habilidade_teste_2.insert_habilidade_banco() 

        
        cls.personagem_teste = PersonagemHabilidades(
            id_usuario=cls.usuario_teste.id,
            id_raca=cls.raca_teste.id_raca,
            nome_personagem=cls.nome_personagem_teste,
        )
        await cls.personagem_teste.adicionar_personagem_banco()
        
        cls.response_insert_habilidade = await cls.personagem_teste.adicionar_habilidade_banco(cls.habilidade_teste.id_habilidade)
        cls.response_load_habilidade_personagem = await cls.personagem_teste.carregar_habilidades_do_banco()
        
    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_personagem_banco()
        await cls.usuario_teste.delete_usuario()
        await cls.habilidade_teste.delete_habilidade_banco()
        await cls.habilidade_teste_2.delete_habilidade_banco()
        await cls.raca_teste.delete_raca_banco()    
        
    async def test_load_habilidades_true(self):
        self.assertTrue(self.response_load_habilidade_personagem)
       
    async def test_insert_habilidade_personagem_true(self):
        self.assertTrue(self.response_insert_habilidade)
        
    async def test_name_habilidade_equal_name_habilidade_personagem_teste_habilidade(self):
        self.assertEqual(self.habilidade_teste.nome_habilidade, self.personagem_teste.habilidades[0]['nome_habilidade'])   
        
    async def test_update_habilidade_personagem(self):
        self.assertTrue(self.personagem_teste.update_habilidade_banco(id_habilidade=self.habilidade_teste_2.id_habilidade, id_habilidade_personagem=self.personagem_teste.habilidade[0]['id_habilidade_personagem']))
        self.assertTrue(self.personagem_teste.carregar_habilidades_do_banco())
        self.assertEqual(self.personagem_teste.habilidade[0]['nome_habilidade'], self.habilidade_teste_2.nome_habilidade)
        
    async def test_habilidade1_dif_habilidade2(self):
        self.assertNotEqual(self.habilidade_teste.nome_habilidade, self.habilidade_teste_2.nome_habilidade)

    async def test_adiconar_habilidade_personagem_habilidades_bigger_equal_2(self):
        self.assertTrue(self.personagem_teste.adicionar_habilidade_banco(id_habilidade=self.habilidade_teste.id_habilidade))
        self.assertTrue(self.personagem_teste.carregar_habilidades_do_banco())
        self.assertTrue(len(self.personagem_teste.habilidades) > 0)
    
if __name__ == '__main__':
    asyncio.run(unittest.main())