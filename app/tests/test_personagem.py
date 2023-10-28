import unittest
from src import User, Character, Race, Classe
import asyncio

class PersonagemTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = User(name='John', email='john@example.com', password='pass123', birth_date='1990-01-01')
        await cls.usuario_teste.insert_user()
        cls.classe_teste = Classe(class_name='Classe_Teste')
        await cls.classe_teste.insert_class()
        cls.classe_teste_UPDATE = Classe(class_name='Classe_Teste_UPDATE')
        await cls.classe_teste_UPDATE.insert_class()
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
        cls.raca_teste_UPDATE = Race(race_name='raca_Teste_UPDATE')
        await cls.raca_teste_UPDATE.insert_race()
        cls.personagem_teste=Character(id_user=cls.usuario_teste.id_user)
        await cls.personagem_teste.insert_character(id_race=cls.raca_teste.id_race,character_name='nome personagem teste')
        

    @classmethod
    async def tearDown(cls):
        for classe in await cls.personagem_teste.classe:
            await cls.personagem_teste.delete_character_class(classe['id_classe_personagem'])  
        
        await cls.classe_teste_UPDATE.delete_class()
        await cls.classe_teste.delete_class()
        await cls.personagem_teste.delete_character()
        await cls.raca_teste.delete_race()
        await cls.raca_teste_UPDATE.delete_race()
        await cls.usuario_teste.delete_user() 
        
    async def test_nome_personagem(self):
        self.assertEqual(await self.personagem_teste.character_name, 'nome personagem teste')
        
    async def test_novo_nome_personagem(self):
        await self.personagem_teste.update_character(chave='nome_personagem',valor='novo nome personagem teste')
        await self.personagem_teste.load_character()
        self.assertEqual(await self.personagem_teste.character_name, 'novo nome personagem teste')
        
    async def test_raca_personagem(self):
        self.assertEqual(await self.personagem_teste.race, 'raca_Teste')
        
    async def test_update_raca(self):
        await self.personagem_teste.update_character(chave='id_raca',valor=self.raca_teste_UPDATE.id_race)
        await self.personagem_teste.load_character()
        self.assertTrue(await self.personagem_teste.race, await self.raca_teste_UPDATE.race_name)
    
    async def test_atribuicao_classe(self):
        await self.personagem_teste.insert_character_class(id_class=self.classe_teste.id_class)
        self.assertTrue(any(classe['id_classe'] == self.classe_teste.id_class for classe in await self.personagem_teste.classes))
        
    async def test_update_classe(self):
        id_classe_personagem = self.personagem_teste.classes[0]['id_classe_personagem']
        await self.personagem_teste.update_character_class(id_classe_personagem=id_classe_personagem, id_classe=self.classe_teste_UPDATE.id_class)
        await self.personagem_teste.load_character_classes()
        self.assertTrue(any(classe['id_classe'] == self.classe_teste_UPDATE.id_class for classe in await self.personagem_teste.classes))

    async def test_carregar_classes_usuarios_banco(self):
        self.assertTrue(self.personagem_teste.load_character_classes())
        self.assertGreater(len(self.personagem_teste.classe), 0)
    
if __name__ == '__main__':
    asyncio.run(unittest.main())