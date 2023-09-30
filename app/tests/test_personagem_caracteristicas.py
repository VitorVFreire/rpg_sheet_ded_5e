import unittest
from src import PersonagemCaracteristicas, Usuario, Raca, Habilidade
import asyncio

class PersonagemCaracteristicasTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = Usuario(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        await cls.usuario_teste.create_usuario()
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        await cls.raca_teste.insert_raca_banco()
        cls.nome_personagem_teste = 'Personagem de Teste'
        
        cls.personagem_teste = PersonagemCaracteristicas(
            id_usuario=cls.usuario_teste.id,
            id_raca=cls.raca_teste.id_raca,
            nome_personagem=cls.nome_personagem_teste,
        )
        cls.response_insert_personagem = await cls.personagem_teste.adicionar_personagem_banco()  
        cls.response_insert_carct = await cls.personagem_teste.adicionar_caracteristicas_banco(chave='idade', valor=10)   
        cls.response_load_caract = await cls.personagem_teste.carregar_caracteristicas_do_banco()  
   
    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_personagem_banco()
        await cls.usuario_teste.delete_usuario()
        await cls.raca_teste.delete_raca_banco()  
        
    async def test_exists_caracteristica_bank_false(self):
        self.assertFalse(self.personagem_teste.exists_caracteristicas_banco()) 
        
    async def test_personagem_criado_true(self):
        self.assertTrue(self.response_insert_personagem)
        
    async def test_caracteristica_insert_bank_true(self):
        self.assertTrue(self.response_insert_carct)
       
    async def test_load_caracteristicas_personagem_true(self):
        self.assertTrue(self.response_load_caract)
        
    async def test_idade_10(self):
        self.assertEqual(self.personagem_teste.idade, 10)
        
    async def test_update_idade_20(self):
        self.assertTrue(self.personagem_teste.update_caracteristicas_banco(chave='idade', valor=20))
        self.assertTrue(self.personagem_teste.carregar_caracteristicas_do_banco())
        self.assertEqual(self.personagem_teste.idade, 20)
        self.assertNotEqual(self.personagem_teste, 10)
        
    async def test_update_cor_olhos_vermelho_true(self):
        self.assertTrue(self.personagem_teste.update_caracteristicas_banco(chave='cor_olhos', valor='vermelho'))
        self.assertEqual(self.personagem_teste.cor_olhos, 'vermelho')
        
    async def test_cor_pele_is_none(self):
        self.assertIsNone(self.personagem_teste.cor_pele)
        
    async def test_delete_caracterisca_bank_true(self):
        self.assertTrue(self.personagem_teste.delete_caracteristicas_banco())
                    
if __name__ == '__main__':
    asyncio.run(unittest.main())