import unittest
from data import mydb
from src import Pericia

class PericiaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mydb.connect()  # Conectar ao banco de dados
        cls.pericia_teste = Pericia(nome_pericia='pericia_Teste',status_uso='status_teste')
        cls.pericia_teste.insert_pericia_banco() #Cria uma pericia no banco e espera receber True da criação
        
    @classmethod
    def tearDownClass(cls):
        cls.pericia_teste.delete_pericia_banco()  # Excluir o pericia teste
        mydb.close()  # Fechar a conexão com o banco de dados

    def test_nome_pericia(self):
        # Verificar se o nome da pericia está correta
        self.assertEqual(self.pericia_teste.nome_pericia, 'pericia_Teste')

    def test_update_nome_pericia(self):
        # Atualizar o nome da pericia
        self.pericia_teste.update_pericia_banco(chave='nome_pericia',valor="Nova pericia Teste")
        self.pericia_teste.carregar_pericia()
        self.assertEqual(self.pericia_teste.nome_pericia[0], "Nova pericia Teste")
    
    def test_update_status_pericia(self):
        # Atualizar o status da pericia
        self.assertTrue(self.pericia_teste.update_pericia_banco(chave='status_uso',valor="novo status"))
        self.pericia_teste.carregar_pericia()
        self.assertEqual(self.pericia_teste.status_uso, "novo status")

    def test_carregar_pericias_banco(self):
        # Carregar as pericias do banco de dados
        pericias_teste=Pericia()
        self.assertTrue(pericias_teste.carregar_pericias())
        pericias = pericias_teste.pericias
        self.assertGreater(len(pericias), 0)

if __name__ == '__main__':
    unittest.main()