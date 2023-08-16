import unittest
from data import get_connection
from src import Usuario
import asyncio


class UsuarioTest(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        conn = await get_connection()
        mydb = await conn.cursor()
        await mydb.connect()  # Conectar ao banco de dados
        cls.usuario_teste = Usuario(nome="John", email="john@example.com", senha="pass123", data_nascimento="1990-01-01")
        await cls.usuario_teste.create_usuario()  # Criar um usuário de teste

    @classmethod
    async def tearDownClass(cls):
        await cls.usuario_teste.delete_usuario()  # Excluir o usuário de teste
        await mydb.close()  # Fechar a conexão com o banco de dados

    async def test_valid_usuario(self):
        # O usuário de teste deve ser válido
        await self.assertEqual(await self.usuario_teste.valid_usuario(), True)

    async def test_get_usuario(self):
        # Verificar se as informações do usuário estão corretas
        await self.usuario_teste.get_usuario()
        await self.assertIsNotNone(self.usuario_teste)
        await self.assertEqual(self.usuario_teste.nome, "John")
        await self.assertEqual(self.usuario_teste.email, "john@example.com")

    async def test_update_usuario(self):
        # Atualizar o nome do usuário
        await self.usuario_teste.update_usuario("nome", "John Doe")
        await self.usuario_teste.get_usuario()
        await self.assertIsNotNone(self.usuario_teste.nome)
        await self.assertEqual(self.usuario_teste.nome, "John Doe")

    """async def test_carregar_personagens_banco(self):
        # Carregar os personagens do usuário do banco de dados
        await self.assertTrue(self.usuario_teste.carregar_personagens_banco())
        personagens = self.usuario_teste.personagens
        await self.assertGreater(len(personagens), 0)"""

    async def test_years(self):
        # Verificar a idade do usuário com base em sua data de nascimento
        await self.assertEqual(self.usuario_teste.years, 33)

    async def test_invalid_usuario(self):
        # Testar um usuário inválido
        usuario = Usuario(email="invalid@example.com", senha="invalidpass")
        await self.assertEqual(await usuario.valid_usuario(), False)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(unittest.main())    
    
#python -m unittest -v tests/test_usuario.py


        