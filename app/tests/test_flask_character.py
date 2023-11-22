import unittest
from main import app

class TestNewCharacterView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.response = cls.app.post('/login', data={'email': 'teste@teste', 'password': '123'})
        cls.response_post_insert_personagem = cls.app.post('/insert_personagem', data={
            'id_raca': 1,
            'id_classe': 1,
            'nome_personagem': 'teste_personagem'
        })
        response_data = cls.response_post_insert_personagem.get_json()
        cls.id_personagem = response_data['id_personagem']
        
    @classmethod
    def tearDownClass(cls):
        cls.app.delete(f'/personagem/{cls.id_personagem}')
        
    def test_post_login_usuario_code_302(self):
        self.assertEqual(self.response.status_code, 302)
    
    def test_post_insert_personagem_code_200(self):        
        self.assertIsNotNone(self.id_personagem)
        self.assertEqual(self.response_post_insert_personagem.status_code, 200)

    def test_get_text_personagem_pag(self):
        response_get_personagem_pag = self.app.get('/criar_personagem')
        self.assertIn(b'<input placeholder="Nome Personagem" type="text" class="form-control" name="nome_personagem" id="nome_personagem" required/>', response_get_personagem_pag.data)
        
    def test_get_text_personagens_pag(self):
        response_get_personagens_pag = self.app.get('/personagens')
        string = f'href="/personagem/{self.id_personagem}"'
        self.assertIn(string.encode(), response_get_personagens_pag.data)       

if __name__ == '__main__':
    unittest.main()
