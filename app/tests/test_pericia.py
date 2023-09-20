import unittest
import asyncio
from data import get_connection
from src import Pericia

class PericiaTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.conn = await get_connection()
        cls.mycursor = await cls.conn.cursor()
        await cls.mycursor.connect()  
        cls.pericia_teste = Pericia(nome_pericia='pericia_Teste', status_uso='status_teste')
        await cls.pericia_teste.insert_pericia_banco()

    @classmethod
    async def tearDown(cls):
        await cls.pericia_teste.delete_pericia_banco() 
        await cls.mycursor.close()  
        await cls.conn.close()
        await cls.conn.wait_closed()

    async def test_nome_pericia(self):
        self.assertEqual(self.pericia_teste.nome_pericia, 'pericia_Teste')

    async def test_update_nome_pericia(self):
        await self.pericia_teste.update_pericia_banco(chave='nome_pericia', valor="Nova pericia Teste")
        await self.pericia_teste.carregar_pericia()
        self.assertEqual(self.pericia_teste.nome_pericia, "Nova pericia Teste")

    async def test_update_status_pericia(self):
        self.assertTrue(await self.pericia_teste.update_pericia_banco(chave='status_uso', valor="novo status"))
        await self.pericia_teste.carregar_pericia()
        self.assertEqual(self.pericia_teste.status_uso, "novo status")

    async def test_carregar_pericias_banco(self):
        pericias_teste = Pericia()
        self.assertTrue(await pericias_teste.carregar_pericias())
        pericias = await pericias_teste.pericias
        self.assertGreater(len(pericias), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())
