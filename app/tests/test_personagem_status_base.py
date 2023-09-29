import unittest
from src import PersonagemStatusBase, Usuario, Raca
import asyncio

class PersonagemStatusBaseTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = Usuario(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        await cls.usuario_teste.create_usuario()
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        await cls.raca_teste.insert_raca_banco()
        cls.nome_personagem_teste = 'Personagem de Teste'

        cls.personagem_teste = PersonagemStatusBase(
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
    
    async def test_validar_existencia_status_base_false(self):
        self.assertFalse(await self.personagem_teste.exists_status_base_banco())

    async def test_adicionar_status_base_vida_20(self):
        self.assertTrue(await self.personagem_teste.adicionar_status_base_banco(chave='vida', valor=20))

    async def test_validar_existencia_vida_personagem_true(self):
        self.assertTrue(await self.personagem_teste.exists_status_base_banco())
        
    async def test_vida_personagem_equal_20(self):
        self.assertEqual(await self.personagem_teste.vida, 20)
        
    async def test_update_vida_personagem_true(self):
        self.assertTrue(await self.personagem_teste.update_status_base_banco(chave='vida', valor=10))
    
    async def test_vida_personagem_equal_10(self):
        self.assertEqual(await self.personagem_teste.vida, 10)
        
    async def test_load_status_base_true_vida_10_nivel_none(self):
        status_base = PersonagemStatusBase(id_personagem = self.personagem_teste.id_personagem, id_usuario = self.usuario_teste.id)
        self.assertTrue(await status_base.carregar_status_base_do_banco())
        self.assertEqual(status_base.vida, 10)
        self.assertIsNone(status_base.nivel)
    
    async def test_adicionar_status_base_xp_20(self):
        self.assertTrue(await self.personagem_teste.adicionar_status_base_banco(chave='xp', valor=20))
    
    async def test_load_status_base_true_vida_10_xp_20(self):
        status_base = PersonagemStatusBase(id_personagem = self.personagem_teste.id_personagem, id_usuario = self.usuario_teste.id)
        self.assertTrue(await status_base.carregar_status_base_do_banco())
        self.assertEqual(status_base.vida, 10)
        self.assertEqual(status_base.xp, 10)
         
    async def test_delete_vida_personagem_true(self):
        self.assertTrue(await self.personagem_teste.delete_classe_banco())

if __name__ == '__main__':
    asyncio.run(unittest.main())