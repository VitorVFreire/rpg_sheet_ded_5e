import unittest
from src import Raca
import asyncio

class RacaTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        await cls.raca_teste.insert_raca_banco()
    
    @classmethod
    async def tearDown(cls):
        await cls.raca_teste.delete_raca_banco()          

    async def test_nome_raca(self):
        self.assertEqual(self.raca_teste.nome_raca, 'raca_Teste')

    async def test_update_raca(self):
        await self.raca_teste.update_raca_banco(valor="Nova raca Teste")
        await self.raca_teste.carregar_raca()
        self.assertEqual(self.raca_teste.nome_raca, "Nova raca Teste")

    async def test_carregar_racas_banco(self):
        racas_teste=Raca()
        self.assertTrue(await racas_teste.carregar_racas())
        racas = await racas_teste.racas
        self.assertGreater(len(racas), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())