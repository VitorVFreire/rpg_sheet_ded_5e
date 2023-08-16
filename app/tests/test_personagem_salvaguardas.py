# CRIA SALVAGUARDA TESTE:
        cls.salvaguarda_teste = Salvaguarda(nome_salvaguarda='inteligencia')
        cls.salvaguarda_teste.insert_salvaguarda_banco()
        cls.salvaguarda_teste_UPDATE = Salvaguarda(nome_salvaguarda='forca')
        cls.salvaguarda_teste_UPDATE.insert_salvaguarda_banco()
        
        #DELETA A SALVAGUARDA DE TESTE:
        for salvaguarda in cls.personagem_teste.salvaguardas:
            cls.personagem_teste.delete_salvaguarda_banco(salvaguarda['id_salvaguarda_personagem'])  
            
        cls.salvaguarda_teste.delete_salvaguarda_banco()
        cls.salvaguarda_teste_UPDATE.delete_salvaguarda_banco()
        
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