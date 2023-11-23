import unittest
from src import CharacterSkills, Skill, User, Race
import asyncio

class CharacterSkillTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = User(name='John', email='john@example.com', password='pass123', birth_date='1990-01-01')
        await cls.usuario_teste.insert_user()
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
        cls.nome_personagem_teste = 'Personagem de Teste'

        cls.personagem_teste = CharacterSkills(
            user_id=cls.usuario_teste.user_id,
            race_id=cls.raca_teste.race_id,
            nome_personagem=cls.nome_personagem_teste
        )
        await cls.personagem_teste.insert_character()
        cls.pericia_teste = Skill(skill_name='acrobacia')
        cls.pericia_teste.load_skill_by_name()
        
    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_character()
        await cls.usuario_teste.delete_user()
        await cls.raca_teste.delete_race()
        
        cls.personagem_teste.delete_skills(cls.pericia_teste.id_skill)

        
    async def test_adiciona_pericia_acrobacia_personagem(self):
        self.assertTrue(await self.personagem_teste.insert_skill(self.pericia_teste.id_skill))
        await self.personagem_teste.load_skills()
        self.assertTrue(any(pericia['skill_id'] == self.pericia_teste.id_skill for pericia in self.personagem_teste.skills))
        if self.personagem_teste.proficiency_bonus is not None and self.personagem_teste.strength is not None:
            self.assertEqual(self.personagem_teste.acrobatics,(self.personagem_teste.strength_bonus+self.personagem_teste.proficiency_bonus))

if __name__ == '__main__':
    asyncio.run(unittest.main())