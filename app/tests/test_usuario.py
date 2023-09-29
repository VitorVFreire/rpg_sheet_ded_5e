import unittest
from src import Usuario
import asyncio

class UsuarioTest(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.usuario_teste = Usuario(nome="John", email="john@example.com", senha="pass123", data_nascimento="1990-01-01")
        await cls.usuario_teste.create_usuario()

    @classmethod
    async def tearDownClass(cls):
        await cls.usuario_teste.delete_usuario()

    async def test_valid_usuario(self):
        self.assertEqual(await self.usuario_teste.valid_usuario(), True)

    async def test_get_usuario(self):
        await self.usuario_teste.get_usuario()
        self.assertIsNotNone(self.usuario_teste)
        self.assertEqual(await self.usuario_teste.nome, "John")
        self.assertEqual(await self.usuario_teste.email, "john@example.com")

    async def test_update_usuario(self):
        await self.usuario_teste.update_usuario("nome", "John Doe")
        await self.usuario_teste.get_usuario()
        self.assertIsNotNone(self.usuario_teste.nome)
        self.assertEqual(self.usuario_teste.nome, "John Doe")

    async def test_carregar_personagens_banco(self):
        self.assertTrue(await self.usuario_teste.carregar_personagens_banco())
        personagens = await self.usuario_teste.personagens
        self.assertGreater(len(personagens), 0)

    async def test_years(self):
        self.assertEqual(await self.usuario_teste.idade, 33)

    async def test_invalid_usuario(self):
        usuario = Usuario(email="invalid@example.com", senha="invalidpass")
        self.assertEqual(await usuario.valid_usuario(), False)

if __name__ == '__main__':
    asyncio.run(unittest.main())   
    
#python -m unittest -v tests/test_usuario.py


        