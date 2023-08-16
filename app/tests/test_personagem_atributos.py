#DELETA OS ATRIBUTOS DE TESTE:
        cls.personagem_teste.delete_atributos_banco()
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