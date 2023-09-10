import unittest
import asyncio
from data import get_connection
from src import Classe

class ClasseTest(unittest.TestCase):
    @classmethod
    async def setUp(cls):
        cls.conn = await get_connection()
        cls.mycursor = await cls.conn.cursor()
        await cls.mycursor.connect()  # Conectar ao banco de dados
        cls.classe_teste = Classe(nome_classe='Classe_Teste')
        await cls.classe_teste.insert_classe_banco() # Cria uma Classe no banco e espera receber True da criação

    @classmethod
    async def tearDown(cls):
        await cls.classe_teste.delete_classe_banco()  # Excluir a classe teste
        await cls.mycursor.close()  # Fechar a conexão com o banco de dados
        cls.conn.close()
        await cls.conn.wait_closed()

    def test_nome_classe(self):
        # Verificar se o nome da classe está correto
        print(f'\n\n\n\nNome:{self.classe_teste.nome_classe}\n\n\n\n\n')
        self.assertEqual(self.classe_teste.nome_classe, 'Classe_Teste')

    async def test_update_classe(self):
        # Atualizar o nome da classe
        await self.classe_teste.update_classe_banco(valor="Nova Classe Teste")
        await self.classe_teste.carregar_classe()
        self.assertEqual(self.classe_teste.nome_classe[0], "Nova Classe Teste")

    async def test_carregar_classes_banco(self):
        # Carregar as classes do banco de dados
        classes_teste = Classe()
        await classes_teste.carregar_classes()
        classes = await classes_teste.classes
        self.assertGreater(len(classes), 0)

if __name__ == '__main__':
    asyncio.run(unittest.main())
