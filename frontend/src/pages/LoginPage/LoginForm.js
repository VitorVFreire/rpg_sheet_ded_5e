import './LoginPage.css'
import TextInput from '../../components/TextInput';
import Button from '../../components/Button';

function LoginForm() {
  //const [email, setEmail] = useState('');
  //const [password, setPassword] = useState('');
  {/* value={password} 
            oAlterado={value => setPassword(value)} */}
  {/* value={email}
            aoAlterado={value => setEmail(value)} */}
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
          name="senha"
          label="Senha"
          required={true}
          placeholder="Digite sua senha"
          type="password"
        />
        <Button>
            Entrar
        </Button>
      </form>
    </section >
  );
}

export default LoginForm;