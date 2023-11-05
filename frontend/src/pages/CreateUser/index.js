import Navbar from '../../components/Navbar'
import { useEffect } from 'react';
import RegisterForm from './ResgisterForm';

function CreateUser(props) {
  const idUser = props.idUser;
  useEffect(() => {
    document.title = 'Cadastro de Usuario';
  }, []);
  return (
    <div className='register-page'>
      <Navbar isLoggedIn={idUser} /> 
      <RegisterForm />
    </div>
  );
}

export default CreateUser;