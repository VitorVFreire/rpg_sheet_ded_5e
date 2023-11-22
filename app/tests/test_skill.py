import unittest
import asyncio
from data import get_connection
from src import Skill

class SkillTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.pericia_teste = Skill(skill_name='pericia_Teste', usage_status='status_teste')
        await cls.pericia_teste.insert_skill()

    @classmethod
    async def tearDown(cls):
        await cls.pericia_teste.delete_skill() 

    async def test_nome_pericia(self):
        self.assertEqual(self.pericia_teste.skill_name, 'pericia_Teste')

    async def test_update_nome_pericia(self):
        await self.pericia_teste.update_skill(key='nome_pericia', value="Nova pericia Teste")
        await self.pericia_teste.load_skill()
        self.assertEqual(self.pericia_teste.skill_name, "Nova pericia Teste")

    async def test_update_status_pericia(self):
        self.assertTrue(await self.pericia_teste.update_skill(key='status_uso', value="novo status"))
        await self.pericia_teste.load_skill()
        self.assertEqual(self.pericia_teste.usage_status, "novo status")

    async def test_carregar_pericias_banco(self):
        pericias_teste = Skill()
        self.assertTrue(await pericias_teste.load_skills())
        pericias = await pericias_teste.skills
        self.assertGreater(len(pericias), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())
