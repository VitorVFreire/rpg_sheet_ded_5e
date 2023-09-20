import unittest
from data import get_connection
from src import Usuario
import asyncio


class UsuarioTest(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.conn = await get_connection()
        cls.mycursor = await cls.conn.cursor()
        await cls.mycursor.connect()
        cls.usuario_teste = Usuario(nome="John", email="john@example.com", senha="pass123", data_nascimento="1990-01-01")
        await cls.usuario_teste.create_usuario()  # Criar um usuário de teste

    @classmethod
    async def tearDownClass(cls):
        await cls.usuario_teste.delete_usuario()  # Excluir o usuário de teste
        await cls.mycursor.close()  
        await cls.conn.close()
        await cls.conn.wait_closed()  # Fechar a conexão com o banco de dados

    async def test_valid_usuario(self):
        # O usuário de teste deve ser válido
        self.assertEqual(await self.usuario_teste.valid_usuario(), True)

    async def test_get_usuario(self):
        # Verificar se as informações do usuário estão corretas
        await self.usuario_teste.get_usuario()
        self.assertIsNotNone(self.usuario_teste)
        self.assertEqual(await self.usuario_teste.nome, "John")
        self.assertEqual(await self.usuario_teste.email, "john@example.com")

    async def test_update_usuario(self):
        # Atualizar o nome do usuário
        await self.usuario_teste.update_usuario("nome", "John Doe")
        await self.usuario_teste.get_usuario()
        self.assertIsNotNone(self.usuario_teste.nome)
        self.assertEqual(self.usuario_teste.nome, "John Doe")

    async def test_carregar_personagens_banco(self):
        # Carregar os personagens do usuário do banco de dados
        self.assertTrue(await self.usuario_teste.carregar_personagens_banco())
        personagens = await self.usuario_teste.personagens
        self.assertGreater(len(personagens), 0)

    async def test_years(self):
        # Verificar a idade do usuário com base em sua data de nascimento
        self.assertEqual(await self.usuario_teste.idade, 33)

    async def test_invalid_usuario(self):
        # Testar um usuário inválido
        usuario = Usuario(email="invalid@example.com", senha="invalidpass")
        self.assertEqual(await usuario.valid_usuario(), False)

if __name__ == '__main__':
    asyncio.run(unittest.main())   
    
#python -m unittest -v tests/test_usuario.py


        