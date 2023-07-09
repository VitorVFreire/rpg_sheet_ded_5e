import unittest
from data import mydb
from src import Usuario, Personagem, Raca, Pericia, Classe, Salvaguarda

class PersonagemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mydb.connect()  # Conectar ao banco de dados
        # CRIA USUARIO TESTE:
        cls.usuario_teste = Usuario(nome='John', email='john@example.com', senha='pass123', data_nascimento='1990-01-01')
        cls.usuario_teste.create_usuario()
        # CRIA PERICIA TESTE:
        cls.pericia_teste = Pericia(nome_pericia='acrobacia',status_uso='status_teste')
        cls.pericia_teste.insert_pericia_banco()
        # CRIA SALVAGUARDA TESTE:
        cls.salvaguarda_teste = Salvaguarda(nome_salvaguarda='inteligencia')
        cls.salvaguarda_teste.insert_salvaguarda_banco()
        cls.salvaguarda_teste_UPDATE = Salvaguarda(nome_salvaguarda='forca')
        cls.salvaguarda_teste_UPDATE.insert_salvaguarda_banco()
        # CRIA CLASSE TESTE:
        cls.classe_teste = Classe(nome_classe='Classe_Teste')
        cls.classe_teste.insert_classe_banco()
        # CRIA CLASSE PARA UPDATE PERSONAGEM:
        cls.classe_teste_UPDATE = Classe(nome_classe='Classe_Teste_UPDATE')
        cls.classe_teste_UPDATE.insert_classe_banco()
        # CRIA RACA TESTE:
        cls.raca_teste = Raca(nome_raca='raca_Teste')
        cls.raca_teste.insert_raca_banco()
        # CRIA RACA UPDATE TESTE:
        cls.raca_teste_UPDATE = Raca(nome_raca='raca_Teste_UPDATE')
        cls.raca_teste_UPDATE.insert_raca_banco()
        # CRIA PERSONAGEM:
        cls.personagem_teste=Personagem(id_usuario=cls.usuario_teste.id)
        cls.personagem_teste.adicionar_personagem_banco(id_raca=cls.raca_teste.id_raca,nome_personagem='nome personagem teste')
        

    @classmethod
    def tearDownClass(cls):
        #DELETA AS CLASSES PRESENTES NO PERSONAGEM:
        for classe in cls.personagem_teste.classe:
            cls.personagem_teste.delete_classe_banco(classe['id_classe_personagem'])
        for salvaguarda in cls.personagem_teste.salvaguardas:
            cls.personagem_teste.delete_salvaguarda_banco(salvaguarda['id_salvaguarda_personagem'])    
        
        #DELETA A SALVAGUARDA DE TESTE:
        cls.salvaguarda_teste.delete_salvaguarda_banco()
        cls.salvaguarda_teste_UPDATE.delete_salvaguarda_banco()
        #DELETA OS ATRIBUTOS DE TESTE:
        cls.personagem_teste.delete_atributos_banco()
        #DELETA A PERICIA DE TESTE:
        cls.personagem_teste.delete_pericias_banco(cls.pericia_teste.id_pericia)
        cls.pericia_teste.delete_pericia_banco() 
        
        #DELETA CLASSES TESTE:
        cls.classe_teste_UPDATE.delete_classe_banco()
        cls.classe_teste.delete_classe_banco()
        #DELETA PERSONAGEM TESTE:
        cls.personagem_teste.delete_personagem_banco()
        #DELETA RACAS DE TESTE:
        cls.raca_teste.delete_raca_banco()
        cls.raca_teste_UPDATE.delete_raca_banco()
        #DELETA USUARIO TESTE:
        cls.usuario_teste.delete_usuario() 
        mydb.close()  # Fechar a conexão com o banco de dados
        
    def test_nome_personagem(self):
        # Verificar se o nome do personagem está correta
        self.assertEqual(self.personagem_teste.nome_personagem, 'nome personagem teste')
        
    def test_novo_nome_personagem(self):
        # Verificar se a mudança do nome foi efetivada
        self.personagem_teste.update_personagem_banco(chave='nome_personagem',valor='novo nome personagem teste')
        self.personagem_teste.carregar_personagem_banco()
        self.assertEqual(self.personagem_teste.nome_personagem, 'novo nome personagem teste')
        
    def test_raca_personagem(self):
        # Verificar se o raca do personagem está correta
        self.assertEqual(self.personagem_teste.raca, 'raca_Teste')
        
    def test_update_raca(self):
        # Verificar se a raca é atualizada corretamente no personagem
        self.personagem_teste.update_personagem_banco(chave='id_raca',valor=self.raca_teste_UPDATE.id_raca)
        self.personagem_teste.carregar_personagem_banco()
        self.assertTrue(self.personagem_teste.raca,self.raca_teste_UPDATE.nome_raca)
    
    def test_atribuicao_classe(self):
        # Verificar se a classe é adicionada ao personagem
        self.personagem_teste.adicionar_classe_banco(id_classe=self.classe_teste.id_classe)
        self.assertTrue(any(classe['id_classe'] == self.classe_teste.id_classe for classe in self.personagem_teste.classe))
        
    def test_update_classe(self):
        # Verificar se a classe é atualizada corretamente no personagem
        id_classe_personagem = self.personagem_teste.classe[0]['id_classe_personagem']
        self.personagem_teste.update_classe_banco(id_classe_personagem=id_classe_personagem, id_classe=self.classe_teste_UPDATE.id_classe)
        self.personagem_teste.carregar_classe_do_banco()
        self.assertTrue(any(classe['id_classe'] == self.classe_teste_UPDATE.id_classe for classe in self.personagem_teste.classe))

    def test_carregar_classes_usuarios_banco(self):
        # Carregar as classes do usuario do banco de dados
        self.personagem_teste
        self.assertTrue(self.personagem_teste.carregar_classe_do_banco())
        self.assertGreater(len(self.personagem_teste.classe), 0)
        
    def test_adiciona_atributo_forca_10_personagem(self):
        if self.personagem_teste.exists_atributos_banco():
            self.personagem_teste.update_atributos_banco(chave='forca',valor=10)
        else:
            self.personagem_teste.adicionar_atributo_banco(chave='forca',valor=10)
        self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.forca,10)
    
    def test_existencia_atributos_espera_True(self):
        # Espera receber False pela não existencia de atributos do personagem
        self.assertTrue(self.personagem_teste.exists_atributos_banco())
        
    def test_bonus_forca_personagem_espera_0(self):
        self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.bonus_forca, 0)
        
    def test_update_atributo_forca_16_personagem(self):
        if self.personagem_teste.exists_atributos_banco():
            self.personagem_teste.update_atributos_banco(chave='forca',valor=16)
            self.personagem_teste.carregar_atributos_do_banco()
            self.assertEqual(self.personagem_teste.forca,16)
            self.assertEqual(self.personagem_teste.bonus_forca, 3)
        
    def test_adiciona_atributo_inteligencia_12_personagem(self):
        if self.personagem_teste.exists_atributos_banco():
            self.personagem_teste.update_atributos_banco(chave='inteligencia',valor=12)
        else:
            self.personagem_teste.adicionar_atributo_banco(chave='inteligencia',valor=12)
        self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.inteligencia,12)
        
    def test_bonus_inteligencia_personagem_espera_1(self):
        self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.bonus_inteligencia, 1)
        
    def test_adiciona_atributo_bonus_proficiencia_2_personagem(self):
        if self.personagem_teste.exists_atributos_banco():
            self.personagem_teste.update_atributos_banco(chave='bonus_proficiencia',valor=2)
        else:
            self.personagem_teste.adicionar_atributo_banco(chave='bonus_proficiencia',valor=2)
        self.personagem_teste.carregar_atributos_do_banco()
        self.assertEqual(self.personagem_teste.bonus_proficiencia,2)

    def test_adiciona_pericia_acrobacia_personagem(self):
        self.assertTrue(self.personagem_teste.adicionar_pericias_banco(self.pericia_teste.id_pericia))
        self.personagem_teste.carregar_pericias_do_banco()
        self.assertTrue(any(pericia['id_pericia'] == self.pericia_teste.id_pericia for pericia in self.personagem_teste.pericias))
        if self.personagem_teste.bonus_proficiencia is not None and self.personagem_teste.forca is not None:
            self.assertEqual(self.personagem_teste.acrobacia,(self.personagem_teste.bonus_forca+self.personagem_teste.bonus_proficiencia))
    
    def test_atribuicao_salvaguarda(self):
        # Verificar se a salvaguarda é adicionada ao personagem
        self.assertEqual(self.salvaguarda_teste.nome_salvaguarda,'inteligencia')
        self.assertTrue(self.personagem_teste.adicionar_salvaguardas_banco(id_salvaguarda=self.salvaguarda_teste.id_salvaguarda))
        self.personagem_teste.carregar_salvaguardas_do_banco()
        self.assertTrue(any(salvaguarda['id_salvaguarda'] == self.salvaguarda_teste.id_salvaguarda for salvaguarda in self.personagem_teste.salvaguardas))
        self.assertEqual(self.personagem_teste.resistencia_inteligencia,(self.personagem_teste.bonus_inteligencia + self.personagem_teste.bonus_proficiencia))
        
    def test_update_salvaguarda(self):
        # Verificar se a salvaguarda é atualizada corretamente no personagem
        id_salvaguarda_personagem = self.personagem_teste.salvaguardas[0]['id_salvaguarda_personagem']
        print()
        self.assertEqual(self.salvaguarda_teste_UPDATE.nome_salvaguarda,'forca')
        self.personagem_teste.update_salvaguardas_banco(id_salvaguarda_personagem=id_salvaguarda_personagem, id_salvaguarda=self.salvaguarda_teste_UPDATE.id_salvaguarda)
        self.personagem_teste.carregar_salvaguardas_do_banco()
        self.assertTrue(any(salvaguarda['id_salvaguarda'] == self.salvaguarda_teste_UPDATE.id_salvaguarda for salvaguarda in self.personagem_teste.salvaguardas))
        self.assertEqual(self.personagem_teste.resistencia_forca,(self.personagem_teste.bonus_forca + self.personagem_teste.bonus_proficiencia))
        
    def test_carregar_salvaguardas_usuarios_banco(self):
        # Carregar as salvaguardas do usuario do banco de dados
        self.personagem_teste
        self.assertTrue(self.personagem_teste.carregar_salvaguardas_do_banco())
        self.assertGreater(len(self.personagem_teste.salvaguardas), 0)
    
if __name__ == '__main__':
    unittest.main()