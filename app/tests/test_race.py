import unittest
from src import Race
import asyncio

class RaceTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
    
    @classmethod
    async def tearDown(cls):
        await cls.raca_teste.delete_race()          

    async def test_nome_raca(self):
        self.assertEqual(self.raca_teste.race_name, 'raca_Teste')

    async def test_update_raca(self):
        await self.raca_teste.update_race(value="Nova raca Teste")
        await self.raca_teste.load_race()
        self.assertEqual(self.raca_teste.race_name, "Nova raca Teste")

    async def test_carregar_racas_banco(self):
        racas_teste=Race()
        self.assertTrue(await racas_teste.load_races())
        racas = await racas_teste.races
        self.assertGreater(len(racas), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())