import unittest
from src import PersonagemAtributos, Usuario, Raca
import asyncio

class PersonagemAtributosTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = Usuario(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        await cls.usuario_teste.create_usuario()
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        await cls.raca_teste.insert_raca_banco()
        cls.nome_personagem_teste = 'Personagem de Teste'

        cls.personagem_teste = PersonagemAtributos(
            id_usuario=cls.usuario_teste.id,
            id_raca=cls.raca_teste.id_raca,
            nome_personagem=cls.nome_personagem_teste
        )
        await cls.personagem_teste.adicionar_personagem_banco()
        
    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_personagem_banco()
        await cls.usuario_teste.delete_usuario()
        await cls.raca_teste.delete_raca_banco()
        
    async def test_adiciona_atributo_forca_10_personagem(self):
        if await self.personagem_teste.exists_atributos_banco():
            await self.personagem_teste.update_atributos_banco(chave='forca',valor=10)
        else:
            await self.personagem_teste.adicionar_atributo_banco(chave='forca',valor=10)
        await self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.forca,10)
    
    async def test_existencia_atributos_espera_True(self):
        self.assertTrue(await self.personagem_teste.exists_atributos_banco())
        
    async def test_bonus_forca_personagem_espera_0(self):
        await self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.bonus_forca, 0)
        
    async def test_update_atributo_forca_16_personagem(self):
        if await self.personagem_teste.exists_atributos_banco():
            await self.personagem_teste.update_atributos_banco(chave='forca',valor=16)
            await self.personagem_teste.carregar_atributos_do_banco()
            self.assertEqual(self.personagem_teste.forca,16)
            self.assertEqual(self.personagem_teste.bonus_forca, 3)
        
    async def test_adiciona_atributo_inteligencia_12_personagem(self):
        if await self.personagem_teste.exists_atributos_banco():
            await self.personagem_teste.update_atributos_banco(chave='inteligencia',valor=12)
        else:
            await self.personagem_teste.adicionar_atributo_banco(chave='inteligencia',valor=12)
        await self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.inteligencia,12)
        
    async def test_bonus_inteligencia_personagem_espera_1(self):
        self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.bonus_inteligencia, 1)
        
    async def test_adiciona_atributo_bonus_proficiencia_2_personagem(self):
        if await self.personagem_teste.exists_atributos_banco():
            await self.personagem_teste.update_atributos_banco(chave='bonus_proficiencia',valor=2)
        else:
            await self.personagem_teste.adicionar_atributo_banco(chave='bonus_proficiencia',valor=2)
        await self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.bonus_proficiencia,2)
        
if __name__ == '__main__':
    asyncio.run(unittest.main())