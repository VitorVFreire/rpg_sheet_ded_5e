import unittest
from src import User
import asyncio

class UserTest(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.usuario_teste = User(name="John", email="john@example.com", password="pass123", birth_date="1990-01-01")
        await cls.usuario_teste.insert_user()

    @classmethod
    async def tearDownClass(cls):
        await cls.usuario_teste.delete_user()

    async def test_valid_usuario(self):
        self.assertEqual(await self.usuario_teste.valid_user(), True)

    async def test_get_usuario(self):
        await self.usuario_teste.load_user()
        self.assertIsNotNone(self.usuario_teste)
        self.assertEqual(await self.usuario_teste.name, "John")
        self.assertEqual(await self.usuario_teste.email, "john@example.com")

    async def test_update_usuario(self):
        await self.usuario_teste.update_user("nome", "John Doe")
        await self.usuario_teste.load_user()
        self.assertIsNotNone(self.usuario_teste.name)
        self.assertEqual(self.usuario_teste.name, "John Doe")

    async def test_carregar_personagens_banco(self):
        self.assertTrue(await self.usuario_teste.load_characters())
        personagens = await self.usuario_teste.characters
        self.assertGreater(len(personagens), 0)

    async def test_years(self):
        self.assertEqual(await self.usuario_teste.age, 33)

    async def test_invalid_usuario(self):
        usuario = User(email="invalid@example.com", password="invalidpass")
        self.assertEqual(await usuario.valid_user(), False)

if __name__ == '__main__':
    asyncio.run(unittest.main())   
    
#python -m unittest -v tests/test_usuario.py


        