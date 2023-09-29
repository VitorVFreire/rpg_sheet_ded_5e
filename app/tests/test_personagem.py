import unittest
from src import Usuario, Personagem, Raca, Classe
import asyncio

class PersonagemTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = Usuario(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        await cls.usuario_teste.create_usuario()
        cls.classe_teste = Classe(nome_classe='Classe_Teste')
        await cls.classe_teste.insert_classe_banco()
        cls.classe_teste_UPDATE = Classe(nome_classe='Classe_Teste_UPDATE')
        await cls.classe_teste_UPDATE.insert_classe_banco()
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        await cls.raca_teste.insert_raca_banco()
        cls.raca_teste_UPDATE = Raca(nome_raca='raca_Teste_UPDATE')
        await cls.raca_teste_UPDATE.insert_raca_banco()
        cls.personagem_teste=Personagem(id_usuario=cls.usuario_teste.id)
        await cls.personagem_teste.adicionar_personagem_banco(id_raca=cls.raca_teste.id_raca,nome_personagem='nome personagem teste')
        

    @classmethod
    async def tearDown(cls):
        for classe in await cls.personagem_teste.classe:
            await cls.personagem_teste.delete_classe_banco(classe['id_classe_personagem'])  
        
        await cls.classe_teste_UPDATE.delete_classe_banco()
        await cls.classe_teste.delete_classe_banco()
        await cls.personagem_teste.delete_personagem_banco()
        await cls.raca_teste.delete_raca_banco()
        await cls.raca_teste_UPDATE.delete_raca_banco()
        await cls.usuario_teste.delete_usuario() 
        
    async def test_nome_personagem(self):
        self.assertEqual(await self.personagem_teste.nome_personagem, 'nome personagem teste')
        
    async def test_novo_nome_personagem(self):
        await self.personagem_teste.update_personagem_banco(chave='nome_personagem',valor='novo nome personagem teste')
        await self.personagem_teste.carregar_personagem_banco()
        self.assertEqual(await self.personagem_teste.nome_personagem, 'novo nome personagem teste')
        
    async def test_raca_personagem(self):
        self.assertEqual(await self.personagem_teste.raca, 'raca_Teste')
        
    async def test_update_raca(self):
        await self.personagem_teste.update_personagem_banco(chave='id_raca',valor=self.raca_teste_UPDATE.id_raca)
        await self.personagem_teste.carregar_personagem_banco()
        self.assertTrue(await self.personagem_teste.raca, await self.raca_teste_UPDATE.nome_raca)
    
    async def test_atribuicao_classe(self):
        await self.personagem_teste.adicionar_classe_banco(id_classe=self.classe_teste.id_classe)
        self.assertTrue(any(classe['id_classe'] == self.classe_teste.id_classe for classe in await self.personagem_teste.classes))
        
    async def test_update_classe(self):
        id_classe_personagem = self.personagem_teste.classes[0]['id_classe_personagem']
        await self.personagem_teste.update_classe_banco(id_classe_personagem=id_classe_personagem, id_classe=self.classe_teste_UPDATE.id_classe)
        await self.personagem_teste.carregar_classes_do_banco()
        self.assertTrue(any(classe['id_classe'] == self.classe_teste_UPDATE.id_classe for classe in await self.personagem_teste.classes))

    async def test_carregar_classes_usuarios_banco(self):
        self.assertTrue(self.personagem_teste.carregar_classes_do_banco())
        self.assertGreater(len(self.personagem_teste.classe), 0)
    
if __name__ == '__main__':
    asyncio.run(unittest.main())