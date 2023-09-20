import unittest
from data import get_connection
from src import Salvaguarda
import asyncio

class SalvaguardaTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.conn = await get_connection()
        cls.mycursor = await cls.conn.cursor()
        await cls.mycursor.connect()  
        cls.salvaguarda_teste = Salvaguarda(nome_salvaguarda='inteligencia')
        await cls.salvaguarda_teste.insert_salvaguarda_banco() #Cria uma salvaguarda no banco e espera receber True da criação
        
    @classmethod
    async def tearDown(cls):
        await cls.salvaguarda_teste.delete_salvaguarda_banco()
        await cls.mycursor.close()  
        await cls.conn.close()
        await cls.conn.wait_closed()

    async def test_nome_salvaguarda(self):
        # Verificar se o nome da salvaguarda está correta
        self.assertEqual(self.salvaguarda_teste.nome_salvaguarda, 'inteligencia')

    async def test_update_salvaguarda(self):
        # Atualizar o nome da salvaguarda
        await self.salvaguarda_teste.update_salvaguarda_banco(valor='forca')
        await self.salvaguarda_teste.carregar_salvaguarda()
        self.assertEqual(self.salvaguarda_teste.nome_salvaguarda, 'forca')

    async def test_carregar_salvaguardas_banco(self):
        # Carregar as salvaguardas do banco de dados
        salvaguardas_teste = Salvaguarda()
        self.assertTrue(await salvaguardas_teste.carregar_salvaguardas())
        salvaguardas = salvaguardas_teste.salvaguardas
        self.assertGreater(len(salvaguardas), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())