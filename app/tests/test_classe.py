import unittest
import asyncio
from src import Classe

class ClasseTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.classe_teste = Classe(class_name='Classe_Teste')
        await cls.classe_teste.insert_class()  
        
    @classmethod
    async def tearDown(cls):
        await cls.classe_teste.delete_class()  

    async def test_nome_classe(self):
        self.assertEqual(self.classe_teste.name_class, 'Classe_Teste')

    async def test_update_classe(self):
        await self.classe_teste.update_class(value="Nova Classe Teste")
        await self.classe_teste.load_class()
        self.assertEqual(self.classe_teste.name_class[0], "Nova Classe Teste")

    async def test_carregar_classes_banco(self):
        classes_teste = Classe()
        await classes_teste.load_classes()
        classes = await classes_teste.classes
        self.assertGreater(len(classes), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())
