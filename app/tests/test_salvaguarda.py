import unittest
from src import Salvaguarda
import asyncio

class SalvaguardaTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.salvaguarda_teste = Salvaguarda(nome_salvaguarda='inteligencia')
        await cls.salvaguarda_teste.insert_salvaguarda_banco()
        
    @classmethod
    async def tearDown(cls):
        await cls.salvaguarda_teste.delete_salvaguarda_banco()

    async def test_nome_salvaguarda(self):
        self.assertEqual(self.salvaguarda_teste.nome_salvaguarda, 'inteligencia')

    async def test_update_salvaguarda(self):
        await self.salvaguarda_teste.update_salvaguarda_banco(valor='forca')
        await self.salvaguarda_teste.carregar_salvaguarda()
        self.assertEqual(self.salvaguarda_teste.nome_salvaguarda, 'forca')

    async def test_carregar_salvaguardas_banco(self):
        salvaguardas_teste = Salvaguarda()
        self.assertTrue(await salvaguardas_teste.carregar_salvaguardas())
        salvaguardas = salvaguardas_teste.salvaguardas
        self.assertGreater(len(salvaguardas), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())