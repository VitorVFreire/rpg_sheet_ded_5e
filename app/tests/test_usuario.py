import unittest
from data import mydb
from src import Usuario

class UsuarioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mydb.connect()  # Conectar ao banco de dados
        cls.usuario_teste = Usuario(nome="John", email="john@example.com", senha="pass123", data_nascimento="1990-01-01")
        cls.usuario_teste.create_usuario()  # Criar um usuário de teste

    @classmethod
    def tearDownClass(cls):
        cls.usuario_teste.delete_usuario()  # Excluir o usuário de teste
        mydb.close()  # Fechar a conexão com o banco de dados

    def test_valid_usuario(self):
        # O usuário de teste deve ser válido
        self.assertEqual(self.usuario_teste.valid_usuario(), True)

    def test_get_usuario(self):
        # Verificar se as informações do usuário estão corretas
        usuario_info = self.usuario_teste.get_usuario()
        self.assertIsNotNone(usuario_info)
        self.assertEqual(usuario_info["nome"], "John")
        self.assertEqual(usuario_info["email"], "john@example.com")

    def test_update_usuario(self):
        # Atualizar o nome do usuário
        self.usuario_teste.update_usuario("nome", "John Doe")
        usuario_info = self.usuario_teste.get_usuario()
        self.assertIsNotNone(usuario_info)
        self.assertEqual(usuario_info["nome"], "John Doe")

    """def test_carregar_personagens_banco(self):
        # Carregar os personagens do usuário do banco de dados
        self.assertTrue(self.usuario_teste.carregar_personagens_banco())
        personagens = self.usuario_teste.personagens
        self.assertGreater(len(personagens), 0)"""

    def test_years(self):
        # Verificar a idade do usuário com base em sua data de nascimento
        self.assertEqual(self.usuario_teste.years, 33)

    def test_invalid_usuario(self):
        # Testar um usuário inválido
        usuario = Usuario(email="invalid@example.com", senha="invalidpass")
        self.assertEqual(usuario.valid_usuario(), False)

if __name__ == '__main__':
    unittest.main()
    
#python -m unittest -v tests/test_usuario.py


        