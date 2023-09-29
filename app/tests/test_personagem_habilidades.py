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

        cls.personagem_teste = PersonagemHabilidades(
            id_usuario=cls.usuario_teste.id,
            id_raca=cls.raca_teste.id_raca,
            nome_personagem=cls.nome_personagem_teste,
        )
        await cls.personagem_teste.adicionar_personagem_banco()
        
        cls.response_inser_habilidade = await cls.personagem_teste.adicionar_habilidade_banco(cls.habilidade_teste.id_habilidade)
        
    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_personagem_banco()
        await cls.usuario_teste.delete_usuario()
        await cls.habilidade_teste.delete_habilidade_banco()
        await cls.raca_teste.delete_raca_banco()
        
if __name__ == '__main__':
    asyncio.run(unittest.main())