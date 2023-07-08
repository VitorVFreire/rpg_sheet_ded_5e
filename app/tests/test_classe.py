import unittest
from data import mydb
from src import Classe

class ClasseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mydb.connect()  # Conectar ao banco de dados
        cls.classe_teste = Classe(nome_classe='Classe_Teste')
        cls.classe_teste.insert_classe_banco() #Cria uma Classe no banco e espera receber True da criação
        
    @classmethod
    def tearDownClass(cls):
        cls.classe_teste.delete_classe_banco()  # Excluir o classe teste
        mydb.close()  # Fechar a conexão com o banco de dados

    def test_nome_classe(self):
        # Verificar se o nome da classe está correta
        self.assertEqual(self.classe_teste.nome_classe, 'Classe_Teste')

    def test_update_classe(self):
        # Atualizar o nome da classe
        self.classe_teste.update_classe_banco(valor="Nova Classe Teste")
        self.classe_teste.carregar_classe()
        self.assertEqual(self.classe_teste.nome_classe[0], "Nova Classe Teste")

    def test_carregar_classes_banco(self):
        # Carregar as classes do banco de dados
        classes_teste=Classe()
        self.assertTrue(classes_teste.carregar_classes())
        classes = classes_teste.classes
        self.assertGreater(len(classes), 0)

if __name__ == '__main__':
    unittest.main()