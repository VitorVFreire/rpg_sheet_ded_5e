# RPG_sheet

![GitHub](https://img.shields.io/github/license/VIVF0/rpg_sheet_ded_5e)
![GitHub Repo Size](https://img.shields.io/github/repo-size/VIVF0/rpg_sheet_ded_5e)
![GitHub Last Commit](https://img.shields.io/github/last-commit/VIVF0/rpg_sheet_ded_5e)

[![Watch the video](https://github.com/VIVF0/rpg_sheet_ded_5e/blob/main/frontend/public/images/BannerSiteRPGSheet.jpg)](https://youtu.be/hSIbVfeJmO0)

## Online Character Sheet for RPG Dungeons & Dragons 5e
This project presents an online character sheet for the Dungeons & Dragons 5th Edition (D&D 5e) role-playing game, developed in Python. The digital character sheet enables players to effortlessly create and manage their character details, offering easy access and real-time updates during gaming sessions.

## Features
### Character Creation
Players can initiate the character creation process by populating essential fields, including name, race, class, level, attributes, abilities, equipment, etc.

### Sheet Management
Efficiently store and manage character sheets, facilitating seamless updates and swift access to pertinent information.

### Automatic Calculations
The online sheet automates calculations for modified attributes, skill bonuses, hit points, etc., providing a smooth user experience and minimizing calculation errors.

### Interactive Board and Chat
Explore an interactive gaming environment featuring a virtual board and chat functionality. Execute dice rolls with the command: `!r 1d20` (or customize by adjusting the number of dice, sides, and incorporating modifiers like +2 or -1).

## Technologies Used
- **Backend:** Python (3.11.4), Flask, Websocket, APIREST
- **Frontend:** React
- **Database:** PostgreSQL
- **Containerization:** Docker

## Getting Started
### Clone the Repository
```bash
git clone https://github.com/VIVF0/rpg_sheet_ded_5e.git
```

### Create PostgreSQL Container
```bash
sudo docker build -t postegsqlrpgimage .
sudo docker run -d -p 5432:5432 --name postegsqlrpgcontainer postegsqlrpgimage
```

### Navigate to the Project Directory
```bash
cd app
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Create .env File
Create a file named `.env` and add the following details:
```env
USER='rpg'
PASSWORD='123'
DATABASE='rpg'
HOST='HOST'
PORT='5432'
SECRET_KEY='your_key'
```

### Run Database Creation Script
```bash
python data/create_db_postgresql.py
```

### Run the Website
```bash
python main.py
```

Visit http://localhost:8085 in your browser to explore the website!

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the code.

## Ficha Online de RPG D&D 5e
Este é um projeto de uma ficha online para o jogo de RPG Dungeons & Dragons 5ª Edição (D&D 5e), desenvolvida em Python. A ficha online permite que os jogadores criem e gerenciem as fichas de seus personagens de forma digital, facilitando o acesso e a atualização das informações durante as sessões de jogo.

### Funcionalidades
Criação de personagens: Os jogadores podem criar novos personagens preenchendo os campos necessários, como nome, raça, classe, nível, atributos, habilidades, equipamentos, etc.

Gerenciamento de fichas: Os jogadores podem armazenar e gerenciar suas fichas de personagens, permitindo a atualização e o acesso rápido às informações.

Cálculos automáticos: A ficha online realiza os cálculos automáticos para atributos modificados, bônus de habilidades, pontos de vida, etc., proporcionando uma experiência mais fluida e evitando erros de cálculo.

### Tecnologias Utilizadas
- **Backend:** Python (3.11.4), Flask, Websocket, APIREST
- **Frontend:** React
- **Banco de Dados:** PostgreSQL
- **Containerização:** Docker

## Como Executar o Projeto
### Clone o Repositório
```bash
git clone https://github.com/VIVF0/rpg_sheet_ded_5e.git
```

### Crie o Container PostgreSQL
```bash
sudo docker build -t postegsqlrpgimage .
sudo docker run -d -p 5432:5432 --name postegsqlrpgcontainer postegsqlrpgimage
```

### Navegue até o Diretório do Projeto
```bash
cd app
```

### Instale as Dependências
```bash
pip install -r requirements.txt
```

### Crie o Arquivo .env
Crie um arquivo chamado `.env` e adicione as seguintes informações:
```env
USER='rpg'
PASSWORD='123'
DATABASE='rpg'
HOST='HOST'
PORT='5432'
SECRET_KEY='your_key'
```

### Execute o Script de Criação do Banco de Dados
```bash
python data/create_db_postgresql.py
```

### Execute o Site
```bash
python main.py
```

Acesse http://localhost:8085 no seu navegador para explorar o site!

## Licença
Este projeto está licenciado sob a Licença MIT. Sinta-se à vontade para usar, modificar e distribuir o código.
