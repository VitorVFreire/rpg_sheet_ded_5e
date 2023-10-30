import './LoginPage.css'
import Navbar from '../../components/Navbar'
import LoginForm from './LoginForm';
import { useEffect } from 'react';

function LoginPage(props) {
  const idUser = props.idUser;
  useEffect(() => {
    document.title = 'Login';
  }, []);
  return (
    <div className='login-page'>
      <Navbar isLoggedIn={idUser} /> 
      <LoginForm />
    </div>
  );
}

export default LoginPage;