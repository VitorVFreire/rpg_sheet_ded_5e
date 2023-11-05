import './CreateUser.css'
import TextInput from '../../components/TextInput';
import Button from '../../components/Button';

function RegisterForm() {
  return (
    <section className="register_user">
      <form action='/cadastro_usuario' method='POST'>
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
        <TextInput
          name="nome"
          label="Nome"
          required={true}
          placeholder="Digite seu nome"
          type="text"
        />
        <TextInput
          name="data_nascimento"
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