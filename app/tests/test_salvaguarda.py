import unittest
from src import SavingThrow
import asyncio

class SalvaguardaTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.salvaguarda_teste = SavingThrow(saving_throw_name='inteligencia')
        await cls.salvaguarda_teste.insert_saving_throw()
        
    @classmethod
    async def tearDown(cls):
        await cls.salvaguarda_teste.delete_saving_throw()

    async def test_nome_salvaguarda(self):
        self.assertEqual(self.salvaguarda_teste.saving_throw_name, 'inteligencia')

    async def test_update_salvaguarda(self):
        await self.salvaguarda_teste.update_saving_throw(valor='forca')
        await self.salvaguarda_teste.load_saving_throw()
        self.assertEqual(self.salvaguarda_teste.saving_throw_name, 'forca')

    async def test_carregar_salvaguardas_banco(self):
        salvaguardas_teste = SavingThrow()
        self.assertTrue(await salvaguardas_teste.load_saving_throws())
        salvaguardas = salvaguardas_teste.saving_throws
        self.assertGreater(len(salvaguardas), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())