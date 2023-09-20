import unittest
import asyncio
from data import get_connection
from src import Classe

class ClasseTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.conn = await get_connection()
        cls.mycursor = await cls.conn.cursor()
        await cls.mycursor.connect()  
        cls.classe_teste = Classe(nome_classe='Classe_Teste')
        await cls.classe_teste.insert_classe_banco()  
        
    @classmethod
    async def tearDown(cls):
        await cls.classe_teste.delete_classe_banco()  
        await cls.mycursor.close()  
        await cls.conn.close()
        await cls.conn.wait_closed()

    async def test_nome_classe(self):
        self.assertEqual(self.classe_teste.nome_classe, 'Classe_Teste')

    async def test_update_classe(self):
        await self.classe_teste.update_classe_banco(valor="Nova Classe Teste")
        await self.classe_teste.carregar_classe()
        self.assertEqual(self.classe_teste.nome_classe[0], "Nova Classe Teste")

    async def test_carregar_classes_banco(self):
        classes_teste = Classe()
        await classes_teste.carregar_classes()
        classes = await classes_teste.classes
        self.assertGreater(len(classes), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())
