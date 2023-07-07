import pytest
from data import mydb
from src import Usuario

@pytest.fixture(scope="module")
def usuario_teste():
    # Configuração
    mydb.connect()  # Conectar ao banco de dados
    usuario = Usuario(nome="John", email="john@example.com", senha="pass123", data_nascimento="1990-01-01")
    usuario.create_usuario()  # Criar um usuário de teste

    yield usuario

    # Limpeza
    usuario.delete_usuario()  # Excluir o usuário de teste
    mydb.close()  # Fechar a conexão com o banco de dados

def test_valid_usuario(usuario_teste):
    # O usuário de teste deve ser válido
    assert usuario_teste.valid_usuario() == True

def test_get_usuario(usuario_teste):
    # Verificar se as informações do usuário estão corretas
    usuario_info = usuario_teste.get_usuario()
    assert usuario_info is not None
    assert usuario_info["nome"] == "John"
    assert usuario_info["email"] == "john@example.com"

def test_update_usuario(usuario_teste):
    # Atualizar o nome do usuário
    usuario_teste.update_usuario("nome", "John Doe")
    usuario_info = usuario_teste.get_usuario()
    assert usuario_info is not None
    assert usuario_info["nome"] == "John Doe"

def test_carregar_personagens_banco(usuario_teste):
    # Carregar os personagens do usuário do banco de dados
    assert usuario_teste.carregar_personagens_banco() == True,'Sem Personagens no Banco'
    personagens = usuario_teste.personagens
    assert len(personagens) > 0

def test_years(usuario_teste):
    # Verificar a idade do usuário com base em sua data de nascimento
    assert usuario_teste.years == 33

def test_invalid_usuario():
    # Testar um usuário inválido
    usuario = Usuario(email="invalid@example.com", senha="invalidpass")
    assert usuario.valid_usuario() == False


        