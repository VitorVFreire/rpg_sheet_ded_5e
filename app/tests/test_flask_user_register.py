from main import app
import unittest

class TestNewUserView(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = app.test_client()
        self.response = self.app.get('/cadastro_usuario')
        
    def test_get_code_200_cadstro_pag(self):
        self.assertEqual(200, self.response.status_code)
        
    def test_get_text__cadastro_usuario__cadastro_pag(self):
        self.assertIn(b'Cadastro Usuario', self.response.data)
        
    def test_post_form_cadastro_with_corret_data_code_200(self):
        response_post_cadastro = self.app.post('/cadastro_usuario', 
                                            data={
                                                'email': 'user_test@user_test', 
                                                'password': '123',
                                                'nome': 'tester_user',
                                                'data_nascimeto': '2000-02-10'
                                            })
        self.assertEqual(response_post_cadastro.status_code, 200)
    
    def test_delete_user_code_200(self):
        response_delete_user = self.app.delete('/delete/usuario')
        response_data = response_delete_user.get_json()
        self.assertEqual(response_delete_user.status_code, 200)
        self.assertEqual(response_data['message'], 'Conta Encerrada com sucesso!')   
        
if __name__ == '__main__':
    unittest.main()