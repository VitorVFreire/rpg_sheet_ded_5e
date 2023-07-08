import unittest
from data import mydb
from src import Raca

class RacaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mydb.connect()  # Conectar ao banco de dados
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        cls.raca_teste.insert_raca_banco() #Cria uma raca no banco e espera receber True da criação
        
    @classmethod
    def tearDownClass(cls):
        cls.raca_teste.delete_raca_banco()  # Excluir o raca teste
        mydb.close()  # Fechar a conexão com o banco de dados

    def test_nome_raca(self):
        # Verificar se o nome da raca está correta
        self.assertEqual(self.raca_teste.nome_raca, 'raca_Teste')

    def test_update_raca(self):
        # Atualizar o nome da raca
        self.raca_teste.update_raca_banco(valor="Nova raca Teste")
        self.raca_teste.carregar_raca()
        self.assertEqual(self.raca_teste.nome_raca[0], "Nova raca Teste")

    def test_carregar_racas_banco(self):
        # Carregar as racas do banco de dados
        racas_teste=Raca()
        self.assertTrue(racas_teste.carregar_racas())
        racas = racas_teste.racas
        self.assertGreater(len(racas), 0)

if __name__ == '__main__':
    unittest.main()