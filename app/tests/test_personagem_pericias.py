# CRIA PERICIA TESTE:
        cls.pericia_teste = Pericia(nome_pericia='acrobacia',status_uso='status_teste')
        cls.pericia_teste.insert_pericia_banco()
        
        #DELETA A PERICIA DE TESTE:
        cls.personagem_teste.delete_pericias_banco(cls.pericia_teste.id_pericia)
        cls.pericia_teste.delete_pericia_banco() 
        
            def test_adiciona_pericia_acrobacia_personagem(self):
        self.assertTrue(self.personagem_teste.adicionar_pericias_banco(self.pericia_teste.id_pericia))
        self.personagem_teste.carregar_pericias_do_banco()
        self.assertTrue(any(pericia['id_pericia'] == self.pericia_teste.id_pericia for pericia in self.personagem_teste.pericias))
        if self.personagem_teste.bonus_proficiencia is not None and self.personagem_teste.forca is not None:
            self.assertEqual(self.personagem_teste.acrobacia,(self.personagem_teste.bonus_forca+self.personagem_teste.bonus_proficiencia))