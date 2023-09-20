import unittest
from data import get_connection
from src import PersonagemPericias, Pericia, Usuario, Raca
import asyncio

class PersonagemPericiasTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.conn = await get_connection()
        cls.mycursor = await cls.conn.cursor()

        # Cria um personagem de teste com valores não nulos
        cls.usuario_teste = Usuario(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        await cls.usuario_teste.create_usuario()
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        await cls.raca_teste.insert_raca_banco()
        cls.nome_personagem_teste = 'Personagem de Teste'

        cls.personagem_teste = PersonagemPericias(
            id_usuario=cls.usuario_teste.id,
            id_raca=cls.raca_teste.id_raca,
            nome_personagem=cls.nome_personagem_teste
        )
        await cls.personagem_teste.adicionar_personagem_banco()
        # CRIA PERICIA TESTE:
        cls.pericia_teste = Pericia(nome_pericia='acrobacia')
        cls.pericia_teste.carregar_pericia_nome()
        
    @classmethod
    async def tearDown(cls):
        # Exclui o personagem de teste
        await cls.personagem_teste.delete_personagem_banco()
        await cls.usuario_teste.delete_usuario()
        await cls.raca_teste.delete_raca_banco()
        
        #DELETA A PERICIA DE TESTE:
        cls.personagem_teste.delete_pericias_banco(cls.pericia_teste.id_pericia)
        
        # Fecha a conexão e o cursor
        await cls.mycursor.close()
        await cls.conn.close()
        await cls.conn.wait_closed()
        
    async def test_adiciona_pericia_acrobacia_personagem(self):
        self.assertTrue(await self.personagem_teste.adicionar_pericias_banco(self.pericia_teste.id_pericia))
        await self.personagem_teste.carregar_pericias_do_banco()
        self.assertTrue(any(pericia['id_pericia'] == self.pericia_teste.id_pericia for pericia in self.personagem_teste.pericias))
        if self.personagem_teste.bonus_proficiencia is not None and self.personagem_teste.forca is not None:
            self.assertEqual(self.personagem_teste.acrobacia,(self.personagem_teste.bonus_forca+self.personagem_teste.bonus_proficiencia))

if __name__ == '__main__':
    asyncio.run(unittest.main())