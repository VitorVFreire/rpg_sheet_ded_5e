# RPG_sheet

![GitHub](https://img.shields.io/github/license/VIVF0/rpg_sheet_ded_5e)
![GitHub Repo Size](https://img.shields.io/github/repo-size/VIVF0/rpg_sheet_ded_5e)
![GitHub Last Commit](https://img.shields.io/github/last-commit/VIVF0/rpg_sheet_ded_5e)

## Ficha Online de RPG D&D 5e
Este é um projeto de uma ficha online para o jogo de RPG Dungeons & Dragons 5ª Edição (D&D 5e) desenvolvida em Python. A ficha online permite que os jogadores criem e gerenciem as fichas de seus personagens de forma digital, facilitando o acesso e a atualização das informações durante as sessões de jogo.

### Funcionalidades
Criação de personagens: Os jogadores podem criar novos personagens preenchendo os campos necessários, como nome, raça, classe, nível, atributos, habilidades, equipamentos, etc.

Gerenciamento de fichas: Os jogadores podem armazenar e gerenciar suas fichas de personagens, permitindo a atualização e o acesso rápido às informações.

Cálculos automáticos: A ficha online realiza os cálculos automáticos para atributos modificados, bônus de habilidades, pontos de vida, etc., proporcionando uma experiência mais fluida e evitando erros de cálculo.

Requisitos de instalação
Antes de começar, verifique se você tem os seguintes requisitos instalados:

Python 3.11.4: https://www.python.org/downloads/ <br>
Pip (gerenciador de pacotes do Python): https://pip.pypa.io/en/stable/installing/ <br>

## Online Character Sheet for RPG Dungeons & Dragons 5e
This is a project for an online character sheet for the Dungeons & Dragons 5th Edition (D&D 5e) role-playing game, developed in Python. The online character sheet allows players to create and manage their character sheets digitally, making it easier to access and update information during game sessions.

## Features
Character creation: Players can create new characters by filling in the necessary fields, such as name, race, class, level, attributes, abilities, equipment, etc.

Sheet management: Players can store and manage their character sheets, allowing for easy updates and quick access to information.

Automatic calculations: The online sheet performs automatic calculations for modified attributes, skill bonuses, hit points, etc., providing a smoother experience and avoiding calculation errors.

Installation Requirements
Before getting started, make sure you have the following requirements installed:

Python 3.11.4: https://www.python.org/downloads/ <br>
Pip (Python package manager): https://pip.pypa.io/en/stable/installing/ <br>

## Como executar o projeto | Getting Started
##### Clone o repositório para sua máquina local | Clone the repository to your local machine:
```
git clone https://github.com/VIVF0/rpg_sheet_ded_5e.git
```
##### Criar container Postegs | Create container Postegs:
```
sudo docker build -t postegsqlrpgimage .
sudo docker run -d -p 5432:5432 --name postegsqlrpgcontainer postegsqlrpgimage
```
##### Navegue até o diretório do projeto | Navigate to the project directory:
```
cd app
```
##### Instale as dependências do projeto | Install the required dependencies:
```
pip install -r requirements.txt
```
##### Crie um arquivo .env com HOST do seu banco de dados | Create an .env file with HOST from your database:
```
USER = 'rpg'
PASSWORD = '123'
DATABASE = 'rpg'
HOST = 'HOST'
PORT = '5432'
```
##### Adicione SECRET_KEY para o Flask no arquivo .env | Add SECRET_KEY for Flask in .env file:
```
SECRET_KEY = 'your_key'
```
##### Execute o arquivo create_db_postgresql.py para criar o database | Run the create_db_postgresql.py file to create the database:
```
python data/create_db_postgresql.py
```
##### Execute o arquivo main.py para rodar o site | Run the main.py file to run the website:
```
python main.py
```
##### Entre em http://localhost:8085 no seu navegador para usar o Site | Enter http://localhost:8085 in your browser to use the website!

### Licença | License<br>
Este projeto está licenciado sob a licença MIT.<br>This project is licensed under the MIT License. <br>Sinta-se à vontade para usar, modificar e distribuir este código.
