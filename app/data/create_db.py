import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to the MySQL database server
connection = mysql.connector.connect(
    host='localhost',
    user=os.getenv('USER_BASE'),
    password=os.getenv('PASSWORD_BASE'),
)

cursor = connection.cursor()

cursor.execute("DROP DATABASE IF EXISTS RPG1;")

cursor.execute("CREATE DATABASE RPG1;")

cursor.execute("USE RPG1;")

cursor.execute("""CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(45) NOT NULL,
    email VARCHAR(256) NOT NULL,
    senha VARCHAR(200) NOT NULL,
    data_nascimento DATE
);""")

cursor.execute("""CREATE TABLE raca (
    id_raca INT PRIMARY KEY AUTO_INCREMENT,
    nome_raca VARCHAR(45) NOT NULL
);""")

cursor.execute("""CREATE TABLE personagem (
    id_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_raca INT NOT NULL,
    nome_personagem VARCHAR(45) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_raca) REFERENCES raca(id_raca)
);""")

cursor.execute("""CREATE TABLE pericia (
    id_pericia INT PRIMARY KEY AUTO_INCREMENT,
    nome_pericia VARCHAR(45) NOT NULL,
    status_uso VARCHAR(45) NOT NULL
);""")

cursor.execute("""CREATE TABLE pericia_personagem (
    id_pericia_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    id_pericia INT NOT NULL,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem),
    FOREIGN KEY (id_pericia) REFERENCES pericia(id_pericia)
);""")

cursor.execute("""CREATE TABLE atributos (
    id_atributos INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    forca INT,
    destreza INT,
    constituicao INT,
    inteligencia INT,
    sabedoria INT,
    carisma INT,
    bonus_proficiencia INT,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem)
);""")

cursor.execute("""CREATE TABLE status_base (
    id_status_base INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    vida INT,
    xp DOUBLE,
    nivel INT,
    alinhamento VARCHAR(45),
    antecendente VARCHAR(45),
    faccao VARCHAR(45),
    inspiracao INT,
    ca INT,
    iniciativa INT,
    deslocamento INT,
    vida_atual DOUBLE,
    vida_temporaria DOUBLE,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem)
);""")

cursor.execute("""CREATE TABLE salvaguarda (
    id_salvaguarda INT PRIMARY KEY AUTO_INCREMENT,
    nome_salvaguarda VARCHAR(45) NOT NULL
);""")

cursor.execute("""CREATE TABLE salvaguarda_personagem (
    id_salvaguarda_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    id_salvaguarda INT NOT NULL,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem),
    FOREIGN KEY (id_salvaguarda) REFERENCES salvaguarda(id_salvaguarda)
);""")

cursor.execute("""CREATE TABLE caracteristicas_personagem (
    id_caracteristicas_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    idade INT,
    cor_olhos VARCHAR(45),
    cor_pele VARCHAR(45),
    cor_cabelo VARCHAR(45),
    peso FLOAT,
    altura FLOAT,
    imagem_personagem VARCHAR(300),
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem)
);""")

cursor.execute("""CREATE TABLE classe (
    id_classe INT PRIMARY KEY AUTO_INCREMENT,
    nome_classe VARCHAR(45)
);""")

cursor.execute("""CREATE TABLE classe_personagem (
    id_classe_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    id_classe INT NOT NULL,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem),
    FOREIGN KEY (id_classe) REFERENCES classe(id_classe)
);""")

connection.commit()
