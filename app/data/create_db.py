import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host='localhost',
    user=os.getenv('USER_BASE'),
    password=os.getenv('PASSWORD_BASE'),
)

cursor = connection.cursor()

cursor.execute("DROP DATABASE IF EXISTS RPG;")

cursor.execute("CREATE DATABASE RPG;")

cursor.execute("USE RPG;")

cursor.execute("""
CREATE TABLE usuario(
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(45) NOT NULL,
    email VARCHAR(256) NOT NULL,
    password VARCHAR(200) NOT NULL,
    birth_date DATE,
    tipo_usuario VARCHAR(10) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE raca (
    id_raca INT PRIMARY KEY AUTO_INCREMENT,
    nome_raca VARCHAR(45) NOT NULL,
    link_detalhes VARCHAR(300),
    detalhes VARCHAR(200)
);
""")

cursor.execute("""
CREATE TABLE room (
    id_room INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    nome_room VARCHAR(25),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE personagem (
    id_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_raca INT NOT NULL,
    nome_personagem VARCHAR(45) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_raca) REFERENCES raca(id_raca) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE moeda (
  id_moeda INT PRIMARY KEY AUTO_INCREMENT,
  nome_moeda VARCHAR(50) NOT NULL  
);
""")

cursor.execute("""
CREATE TABLE moedas_personagem (
  id_moeda_personagem INT PRIMARY KEY AUTO_INCREMENT,
  id_moeda INT NOT NULL,
  id_personagem INT NOT NULL,
  qtd_moeda FLOAT NOT NULL,
  FOREIGN KEY (id_moeda) REFERENCES moeda(id_moeda) ON DELETE CASCADE,
  FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE
);               
""")

#permissao
#1 - admin
#0 - padrao
cursor.execute("""
CREATE TABLE room_personagem (
    id_room_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    id_room INT NOT NULL,
    permissao INT,
    FOREIGN KEY (id_room) REFERENCES room(id_room) ON DELETE CASCADE,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE message (
    id_message INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    id_room INT NOT NULL,
    message VARCHAR(200) NOT NULL,
    time DATETIME,
    FOREIGN KEY (id_room) REFERENCES room(id_room) ON DELETE CASCADE,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE tipo_equipamento (
    id_tipo_equipamento INT PRIMARY KEY AUTO_INCREMENT,
    nome_tipo_equipamento VARCHAR(50) NOT NULL  
);
""")

cursor.execute("""
CREATE TABLE equipamento (
    id_equipamento INT PRIMARY KEY AUTO_INCREMENT,
    id_tipo_equipamento INT NOT NULL,
    nome_equipamento VARCHAR(100) NOT NULL,
    descricao VARCHAR(250),
    imagem_equipamento VARCHAR(100),
    preco FLOAT,
    id_moeda INT,
    peso FLOAT,
    ca INT,
    dado VARCHAR(25),
    bonus VARCHAR(25),
    FOREIGN KEY (id_tipo_equipamento) REFERENCES tipo_equipamento(id_tipo_equipamento) ON DELETE CASCADE,
    FOREIGN KEY (id_moeda) REFERENCES moeda(id_moeda) ON DELETE CASCADE
);           
""")

cursor.execute("""
CREATE TABLE equipamento_personagem (
    id_equipamento_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_equipamento INT NOT NULL,
    id_personagem INT NOT NULL,
    qtd INT,
    FOREIGN KEY (id_equipamento) REFERENCES equipamento(id_equipamento) ON DELETE CASCADE,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE
);           
""")

cursor.execute("""
CREATE TABLE pericia (
    id_pericia INT PRIMARY KEY AUTO_INCREMENT,
    nome_pericia VARCHAR(45) NOT NULL,
    status_uso VARCHAR(45) NOT NULL,
    link_detalhes VARCHAR(300)
);
""")

cursor.execute("""
CREATE TABLE pericia_personagem (
    id_pericia_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    id_pericia INT NOT NULL,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE,
    FOREIGN KEY (id_pericia) REFERENCES pericia(id_pericia) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE atributos (
    id_atributos INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    forca INT,
    destreza INT,
    constituicao INT,
    inteligencia INT,
    sabedoria INT,
    carisma INT,
    bonus_proficiencia INT,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE status_base (
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
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE salvaguarda (
    id_salvaguarda INT PRIMARY KEY AUTO_INCREMENT,
    nome_salvaguarda VARCHAR(45) NOT NULL,
    link_detalhes VARCHAR(300)
);
""")

cursor.execute("""
CREATE TABLE salvaguarda_personagem (
    id_salvaguarda_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    id_salvaguarda INT NOT NULL,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE,
    FOREIGN KEY (id_salvaguarda) REFERENCES salvaguarda(id_salvaguarda) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE caracteristicas_personagem (
    id_caracteristicas_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    idade INT,
    cor_olhos VARCHAR(45),
    cor_pele VARCHAR(45),
    cor_cabelo VARCHAR(45),
    peso FLOAT,
    altura FLOAT,
    imagem_personagem VARCHAR(300),
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE classe (
    id_classe INT PRIMARY KEY AUTO_INCREMENT,
    nome_classe VARCHAR(45) NOT NULL,
    link_detalhes VARCHAR(300)
);
""")

cursor.execute("""
CREATE TABLE classe_personagem (
    id_classe_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    id_classe INT NOT NULL,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE,
    FOREIGN KEY (id_classe) REFERENCES classe(id_classe) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE habilidade (
    id_habilidade INT PRIMARY KEY AUTO_INCREMENT,
    nome_atributo VARCHAR(20) NOT NULL,
    nome_habilidade VARCHAR(45) NOT NULL,
    nivel_habilidade INT NOT NULL,
    tipo_dano VARCHAR(20),
    qtd_dados INT NOT NULL,
    lados_dados INT NOT NULL,
    adicional_por_nivel INT NOT NULL,
    link_detalhes VARCHAR(300)
);
""")

cursor.execute("""
CREATE TABLE habilidade_classe (
    id_habilidade_classe INT PRIMARY KEY AUTO_INCREMENT,
    id_classe INT NOT NULL,
    id_habilidade INT NOT NULL,
    FOREIGN KEY (id_classe) REFERENCES classe(id_classe) ON DELETE CASCADE,
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE habilidade_personagem (
    id_habilidade_personagem INT PRIMARY KEY AUTO_INCREMENT,
    id_personagem INT NOT NULL,
    id_habilidade INT NOT NULL,
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem) ON DELETE CASCADE,
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade) ON DELETE CASCADE
);
""")

cursor.execute("""
INSERT INTO classe(nome_classe) VALUES('mago');
""")

cursor.execute("""
INSERT INTO moeda(nome_moeda) VALUES('po'),('pp'),('pc'),('pl'),('da'),('pe');
""")

cursor.execute("""
INSERT INTO tipo_equipamento(nome_tipo_equipamento) 
VALUES ('espada'), ('escudo'), ('armadura');
""")

cursor.execute("""
INSERT INTO pericia (nome_pericia, status_uso)
VALUES
    ('acrobacia', 'destreza'),
    ('arcanismo', 'inteligencia'),
    ('atletismo', 'forca'),
    ('atuacao', 'carisma'),
    ('enganacao', 'carisma'),
    ('furtividade', 'destreza'),
    ('historia', 'inteligencia'),
    ('intimidacao', 'carisma'),
    ('intuicao', 'sabedoria'),
    ('investigacao', 'inteligencia'),
    ('lidar_com_animais', 'sabedoria'),
    ('medicina', 'sabedoria'),
    ('natureza', 'inteligencia'),
    ('percepcao', 'sabedoria'),
    ('persuassao', 'carisma'),
    ('prestidigitacao', 'destreza'),
    ('religiao', 'inteligencia'),
    ('sobrevivencia', 'sabedoria');
""")

cursor.execute("""
INSERT INTO raca(nome_raca) VALUES('humano'),('elfo');
""")

cursor.execute("""
INSERT INTO salvaguarda(nome_salvaguarda) VALUES('forca'),('inteligencia'),('sabedoria'),
('destreza'),('carisma'),('constituicao')
""")

#password: 123
cursor.execute("""
INSERT INTO usuario(nome, email, password, birth_date, tipo_usuario)
VALUES('user_teste', 'teste@teste', 'pmWkWSBCL51Bfkhn79xPuKBKHz//H6B+mY6G9/eieuM=', '2023-09-08', 'admin')               
""")


cursor.execute("""
INSERT INTO room(id_usuario, nome_room)
VALUES(1, 'teste_room')               
""")

cursor.execute("""
INSERT INTO personagem(id_usuario, id_raca, nome_personagem)
VALUES(1, 1, 'teste')              
""")

cursor.execute("""
INSERT INTO room_personagem(id_personagem, id_room, permissao)
VALUES(1, 1, 1)               
""")

connection.commit()
