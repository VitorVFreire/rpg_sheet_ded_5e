import './LoginPage.css'
import TextInput from '../../components/TextInput';
import Button from '../../components/Button';
import { Link } from 'react-router-dom';

function LoginForm() {
  return (
    <section className="login">
      <form action='/login' method='POST'>
        <TextInput
          name="email"
          label="Email"
          required={true}
          placeholder="Digite seu email"
          type="text"
        />
        <TextInput
          name="password"
          label="Senha"
          required={true}
          placeholder="Digite sua senha"
          type="password"
        />
        <Link className='link' to='/user_registration'>
          Novo Usuario
        </Link>
        <Button>
          Entrar
        </Button>
      </form>
    </section>
  );
}

export default LoginForm;