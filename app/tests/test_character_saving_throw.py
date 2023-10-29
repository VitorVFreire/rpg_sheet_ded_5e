import unittest
from src import CharacterSavingThrowTest, SavingThrow, User, Race
import asyncio

class CharacterSavingThrowTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = User(name='John', email='john@example.com', password='pass123', birth_date='1990-01-01')
        await cls.usuario_teste.insert_user()
        cls.raca_teste = Race(race_name='raca_Teste')
        await cls.raca_teste.insert_race()
        cls.nome_personagem_teste = 'Personagem de Teste'

        cls.personagem_teste = CharacterSavingThrowTest(
            id_user=cls.usuario_teste.id_user,
            id_raca=cls.raca_teste.id_race,
            nome_personagem=cls.nome_personagem_teste
        )
        await cls.personagem_teste.insert_character()

        cls.salvaguarda_teste = SavingThrow(saving_throw_name='inteligencia')
        await cls.salvaguarda_teste.load_saving_throw_by_name()

    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_character()
        await cls.usuario_teste.delete_user()
        await cls.raca_teste.delete_race()


    async def test_atribuicao_salvaguarda(self):
        self.assertEqual(self.salvaguarda_teste.saving_throw_name, 'inteligencia')
        await self.personagem_teste.insert_attribute(id_salvaguarda=self.salvaguarda_teste.id_saving_throw)
        await self.personagem_teste.load_saving_throws()
        self.assertTrue(any(salvaguarda['id_salvaguarda'] == self.salvaguarda_teste.id_saving_throw for salvaguarda in await self.personagem_teste.saving_throws))
        self.assertEqual(self.personagem_teste.intelligence_resistance, (self.personagem_teste.intelligence_bonus + self.personagem_teste.proficiency_bonus))

    async def test_update_salvaguarda(self):
        id_salvaguarda_personagem = (await self.personagem_teste.saving_throws)[0]['id_salvaguarda_personagem']
        self.salvaguarda_teste_UPDATE = SavingThrow(saving_throw_name='forca')
        await self.salvaguarda_teste_UPDATE.load_saving_throw_by_name()

        self.assertEqual(self.salvaguarda_teste_UPDATE.saving_throw_name, 'forca')
        await self.personagem_teste.update_saving_throw(id_salvaguarda_personagem=id_salvaguarda_personagem, id_salvaguarda=self.salvaguarda_teste_UPDATE.id_saving_throw)
        await self.personagem_teste.load_saving_throws()
        self.assertTrue(any(salvaguarda['id_salvaguarda'] == self.salvaguarda_teste_UPDATE.id_saving_throw for salvaguarda in await self.personagem_teste.saving_throws))
        self.assertEqual(self.personagem_teste.strength_resistance, (self.personagem_teste.strength_bonus + self.personagem_teste.proficiency_bonus))

    async def test_carregar_salvaguardas_usuarios_banco(self):
        await self.personagem_teste.load_saving_throws()
        self.assertGreater(len(await self.personagem_teste.saving_throws), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())