import './CreateUser.css'
import TextInput from '../../components/TextInput';
import Button from '../../components/Button';

function RegisterForm() {
  return (
    <section className="register_user">
      <form action='/user_registration' method='POST'>
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
        <TextInput
          name="user_name"
          label="Nome"
          required={true}
          placeholder="Digite seu nome"
          type="text"
        />
        <TextInput
          name="birth_date"
          label="Data de Nascimento"
          required={true}
          type="date"
        />
        <Button>
            Cadastrar
        </Button>
      </form>
    </section>
  );
}

export default RegisterForm;