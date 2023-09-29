import unittest
from src import PersonagemSalvaguardas, Salvaguarda, Usuario, Raca
import asyncio

class PersonagemSalvaguardaTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.usuario_teste = Usuario(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        await cls.usuario_teste.create_usuario()
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        await cls.raca_teste.insert_raca_banco()
        cls.nome_personagem_teste = 'Personagem de Teste'

        cls.personagem_teste = PersonagemSalvaguardas(
            id_usuario=cls.usuario_teste.id,
            id_raca=cls.raca_teste.id_raca,
            nome_personagem=cls.nome_personagem_teste
        )
        await cls.personagem_teste.adicionar_personagem_banco()

        cls.salvaguarda_teste = Salvaguarda(nome_salvaguarda='inteligencia')
        await cls.salvaguarda_teste.carregar_salvaguarda_nome()

    @classmethod
    async def tearDown(cls):
        await cls.personagem_teste.delete_personagem_banco()
        await cls.usuario_teste.delete_usuario()
        await cls.raca_teste.delete_raca_banco()


    async def test_atribuicao_salvaguarda(self):
        self.assertEqual(self.salvaguarda_teste.nome_salvaguarda, 'inteligencia')
        await self.personagem_teste.adicionar_atributo_banco(id_salvaguarda=self.salvaguarda_teste.id_salvaguarda)
        await self.personagem_teste.carregar_salvaguardas_do_banco()
        self.assertTrue(any(salvaguarda['id_salvaguarda'] == self.salvaguarda_teste.id_salvaguarda for salvaguarda in await self.personagem_teste.salvaguardas))
        self.assertEqual(self.personagem_teste.resistencia_inteligencia, (self.personagem_teste.bonus_inteligencia + self.personagem_teste.bonus_proficiencia))

    async def test_update_salvaguarda(self):
        id_salvaguarda_personagem = (await self.personagem_teste.salvaguardas)[0]['id_salvaguarda_personagem']
        self.salvaguarda_teste_UPDATE = Salvaguarda(nome_salvaguarda='forca')
        await self.salvaguarda_teste_UPDATE.carregar_salvaguarda_nome()

        self.assertEqual(self.salvaguarda_teste_UPDATE.nome_salvaguarda, 'forca')
        await self.personagem_teste.update_salvaguardas_banco(id_salvaguarda_personagem=id_salvaguarda_personagem, id_salvaguarda=self.salvaguarda_teste_UPDATE.id_salvaguarda)
        await self.personagem_teste.carregar_salvaguardas_do_banco()
        self.assertTrue(any(salvaguarda['id_salvaguarda'] == self.salvaguarda_teste_UPDATE.id_salvaguarda for salvaguarda in await self.personagem_teste.salvaguardas))
        self.assertEqual(self.personagem_teste.resistencia_forca, (self.personagem_teste.bonus_forca + self.personagem_teste.bonus_proficiencia))

    async def test_carregar_salvaguardas_usuarios_banco(self):
        await self.personagem_teste.carregar_salvaguardas_do_banco()
        self.assertGreater(len(await self.personagem_teste.salvaguardas), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())