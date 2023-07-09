import unittest
from data import mydb
from src import Salvaguarda

class SalvaguardaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mydb.connect()  # Conectar ao banco de dados
        cls.salvaguarda_teste = Salvaguarda(nome_salvaguarda='inteligencia')
        cls.salvaguarda_teste.insert_salvaguarda_banco() #Cria uma salvaguarda no banco e espera receber True da criação
        
    @classmethod
    def tearDownClass(cls):
        cls.salvaguarda_teste.delete_salvaguarda_banco()  # Excluir o salvaguarda teste
        mydb.close()  # Fechar a conexão com o banco de dados

    def test_nome_salvaguarda(self):
        # Verificar se o nome da salvaguarda está correta
        self.assertEqual(self.salvaguarda_teste.nome_salvaguarda, 'inteligencia')

    def test_update_salvaguarda(self):
        # Atualizar o nome da salvaguarda
        self.salvaguarda_teste.update_salvaguarda_banco(valor='forca')
        self.salvaguarda_teste.carregar_salvaguarda()
        self.assertEqual(self.salvaguarda_teste.nome_salvaguarda[0], 'forca')

    def test_carregar_salvaguardas_banco(self):
        # Carregar as salvaguardas do banco de dados
        salvaguardas_teste=Salvaguarda()
        self.assertTrue(salvaguardas_teste.carregar_salvaguardas())
        salvaguardas = salvaguardas_teste.salvaguardas
        self.assertGreater(len(salvaguardas), 0)

if __name__ == '__main__':
    unittest.main()