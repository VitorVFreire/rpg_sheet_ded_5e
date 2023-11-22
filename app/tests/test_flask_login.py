from main import app
import unittest

class TestLoginView(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = app.test_client()
        self.response = self.app.get('/login')
        
    def test_get_code_200_login_pag(self):
        self.assertEqual(200, self.response.status_code)
        
    def test_get_text_login_in_login_pag(self):
        self.assertIn(b'<h3>Login</h3>', self.response.data)
        
    def test_post_form_login_without_data_code_406(self):
        response_post_login = self.app.post('/login', data={'email': '', 'password': ''})
        self.assertEqual(response_post_login.status_code, 406)
        self.assertEqual(response_post_login.request.path, '/login')
        
    def test_post_form_login_with_corret_data_code_302(self):
        response_post_login = self.app.post('/login', data={'email': 'teste@teste', 'password': '123'})
        self.assertEqual(response_post_login.status_code, 302)
        self.assertEqual(response_post_login.location, '/')
        
    def test_get_logout_code_200(self):
        response_get_logout = self.app.get('/logout')
        self.assertEqual(response_get_logout.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()

