import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Conectar ao banco de dados MySQL
connection = mysql.connector.connect(
    host='localhost',
    user=os.getenv('USER_BASE'),
    password=os.getenv('PASSWORD_BASE'),
)

# Criar o schema RPG
create_schema_query = "CREATE SCHEMA IF NOT EXISTS RPG DEFAULT CHARACTER SET utf8;"
with connection.cursor() as cursor:
    cursor.execute(create_schema_query)
connection.commit()

# Usar o schema RPG
use_schema_query = "USE RPG;"
with connection.cursor() as cursor:
    cursor.execute(use_schema_query)
connection.commit()

# Tabela usuario
drop_usuario_table_query = "DROP TABLE IF EXISTS RPG.usuario;"
with connection.cursor() as cursor:
    cursor.execute(drop_usuario_table_query)
connection.commit()

create_usuario_table_query = """
CREATE TABLE IF NOT EXISTS RPG.usuario (
  id_usuario INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(45) NOT NULL,
  email VARCHAR(256) NOT NULL,
  senha VARCHAR(200) NOT NULL,
  data_nascimento DATE NULL,
  tipo_usuario VARCHAR(20) NOT NULL,
  PRIMARY KEY (id_usuario)
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_usuario_table_query)
connection.commit()

create_usuario_index_query = "CREATE UNIQUE INDEX email_UNIQUE ON RPG.usuario (email) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_usuario_index_query)
connection.commit()

# Tabela raca
drop_raca_table_query = "DROP TABLE IF EXISTS RPG.raca;"
with connection.cursor() as cursor:
    cursor.execute(drop_raca_table_query)
connection.commit()

create_raca_table_query = """
CREATE TABLE IF NOT EXISTS RPG.raca (
  id_raca INT NOT NULL AUTO_INCREMENT,
  nome_raca VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_raca)
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_raca_table_query)
connection.commit()

create_raca_index_query = "CREATE UNIQUE INDEX nome_raca_UNIQUE ON RPG.raca (nome_raca) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_raca_index_query)
connection.commit()

# Tabela personagem
drop_personagem_table_query = "DROP TABLE IF EXISTS RPG.personagem;"
with connection.cursor() as cursor:
    cursor.execute(drop_personagem_table_query)
connection.commit()

create_personagem_table_query = """
CREATE TABLE IF NOT EXISTS RPG.personagem (
  id_personagem INT NOT NULL AUTO_INCREMENT,
  id_usuario INT NOT NULL,
  id_raca INT NOT NULL,
  nome_personagem VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_personagem),
  CONSTRAINT fk_personagem_usuario FOREIGN KEY (id_usuario) REFERENCES RPG.usuario (id_usuario) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_personagem_raca1 FOREIGN KEY (id_raca) REFERENCES RPG.raca (id_raca) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_personagem_table_query)
connection.commit()

create_personagem_index_query = "CREATE INDEX fk_personagem_usuario_idx ON RPG.personagem (id_usuario) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_personagem_index_query)
connection.commit()

create_personagem_index_query = "CREATE INDEX fk_personagem_raca1_idx ON RPG.personagem (id_raca) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_personagem_index_query)
connection.commit()

# Tabela classe
drop_classe_table_query = "DROP TABLE IF EXISTS RPG.classe;"
with connection.cursor() as cursor:
    cursor.execute(drop_classe_table_query)
connection.commit()

create_classe_table_query = """
CREATE TABLE IF NOT EXISTS RPG.classe (
  id_classe INT NOT NULL AUTO_INCREMENT,
  nome_classe VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_classe)
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_classe_table_query)
connection.commit()

create_classe_index_query = "CREATE UNIQUE INDEX nome_classe_UNIQUE ON RPG.classe (nome_classe) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_classe_index_query)
connection.commit()

# Tabela classe_personagem
drop_classe_personagem_table_query = "DROP TABLE IF EXISTS RPG.classe_personagem;"
with connection.cursor() as cursor:
    cursor.execute(drop_classe_personagem_table_query)
connection.commit()

create_classe_personagem_table_query = """
CREATE TABLE IF NOT EXISTS RPG.classe_personagem (
  id_classe_personagem INT NOT NULL,
  id_personagem INT NOT NULL,
  id_classe INT NOT NULL,
  PRIMARY KEY (id_classe_personagem),
  CONSTRAINT fk_classes_personagem_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_classes_personagem_classe1 FOREIGN KEY (id_classe) REFERENCES RPG.classe (id_classe) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_classe_personagem_table_query)
connection.commit()

create_classe_personagem_index_query = "CREATE INDEX fk_classes_personagem_personagem1_idx ON RPG.classe_personagem (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_classe_personagem_index_query)
connection.commit()

create_classe_personagem_index_query = "CREATE INDEX fk_classes_personagem_classe1_idx ON RPG.classe_personagem (id_classe) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_classe_personagem_index_query)
connection.commit()

# Tabela atributos
drop_atributos_table_query = "DROP TABLE IF EXISTS RPG.atributos;"
with connection.cursor() as cursor:
    cursor.execute(drop_atributos_table_query)
connection.commit()

create_atributos_table_query = """
CREATE TABLE IF NOT EXISTS RPG.atributos (
  id_atributos INT NOT NULL AUTO_INCREMENT,
  id_personagem INT NOT NULL,
  forca INT NULL,
  destreza INT NULL,
  constituicao INT NULL,
  inteligencia INT NULL,
  sabedoria INT NULL,
  carisma INT NULL,
  bonus_proficiencia INT NULL,
  PRIMARY KEY (id_atributos),
  CONSTRAINT fk_atributos_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_atributos_table_query)
connection.commit()

create_atributos_index_query = "CREATE INDEX fk_atributos_personagem1_idx ON RPG.atributos (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_atributos_index_query)
connection.commit()

create_atributos_index_query = "CREATE UNIQUE INDEX id_personagem_UNIQUE ON RPG.atributos (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_atributos_index_query)
connection.commit()

# Tabela pericia
drop_pericia_table_query = "DROP TABLE IF EXISTS RPG.pericia;"
with connection.cursor() as cursor:
    cursor.execute(drop_pericia_table_query)
connection.commit()

create_pericia_table_query = """
CREATE TABLE IF NOT EXISTS RPG.pericia (
  id_pericia INT NOT NULL AUTO_INCREMENT,
  nome_pericia VARCHAR(45) NOT NULL,
  status_uso VARCHAR(45) NULL,
  PRIMARY KEY (id_pericia)
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_pericia_table_query)
connection.commit()

# Tabela pericia_personagem
drop_pericia_personagem_table_query = "DROP TABLE IF EXISTS RPG.pericia_personagem;"
with connection.cursor() as cursor:
    cursor.execute(drop_pericia_personagem_table_query)
connection.commit()

create_pericia_personagem_table_query = """
CREATE TABLE IF NOT EXISTS RPG.pericia_personagem (
  id_pericia_personagem INT NOT NULL AUTO_INCREMENT,
  id_pericia INT NOT NULL,
  id_personagem INT NOT NULL,
  PRIMARY KEY (id_pericia_personagem),
  CONSTRAINT fk_perificia_personagem_pericia1 FOREIGN KEY (id_pericia) REFERENCES RPG.pericia (id_pericia) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_perificia_personagem_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_pericia_personagem_table_query)
connection.commit()

create_pericia_personagem_index_query = "CREATE INDEX fk_perificia_personagem_pericia1_idx ON RPG.pericia_personagem (id_pericia) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_pericia_personagem_index_query)
connection.commit()

create_pericia_personagem_index_query = "CREATE INDEX fk_perificia_personagem_personagem1_idx ON RPG.pericia_personagem (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_pericia_personagem_index_query)
connection.commit()

# Tabela espaco_magia
drop_espaco_magia_table_query = "DROP TABLE IF EXISTS RPG.espaco_magia;"
with connection.cursor() as cursor:
    cursor.execute(drop_espaco_magia_table_query)
connection.commit()

create_espaco_magia_table_query = """
CREATE TABLE IF NOT EXISTS RPG.espaco_magia (
  id_espaco_magia INT NOT NULL AUTO_INCREMENT,
  id_personagem INT NOT NULL,
  nivel_magia INT NOT NULL,
  qtd_utilizado INT NULL,
  PRIMARY KEY (id_espaco_magia),
  CONSTRAINT fk_espaco_magia_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_espaco_magia_table_query)
connection.commit()

create_espaco_magia_index_query = "CREATE INDEX fk_espaco_magia_personagem1_idx ON RPG.espaco_magia (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_espaco_magia_index_query)
connection.commit()

# Tabela caracteristicas_personagem
drop_caracteristicas_personagem_table_query = "DROP TABLE IF EXISTS RPG.caracteristicas_personagem;"
with connection.cursor() as cursor:
    cursor.execute(drop_caracteristicas_personagem_table_query)
connection.commit()

create_caracteristicas_personagem_table_query = """
CREATE TABLE IF NOT EXISTS RPG.caracteristicas_personagem (
  id_caracteristicas_personagem INT NOT NULL AUTO_INCREMENT,
  id_personagem INT NOT NULL,
  idade INT NULL,
  cor_olhos VARCHAR(45) NULL,
  cor_pele VARCHAR(45) NULL,
  cor_cabelo VARCHAR(45) NULL,
  peso FLOAT NULL,
  altura FLOAT NULL,
  imagem_personagem VARCHAR(300) NULL,
  PRIMARY KEY (id_caracteristicas_personagem),
  CONSTRAINT fk_caracteristicas_personagem_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_caracteristicas_personagem_table_query)
connection.commit()

create_caracteristicas_personagem_index_query = "CREATE INDEX fk_caracteristicas_personagem_personagem1_idx ON RPG.caracteristicas_personagem (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_caracteristicas_personagem_index_query)
connection.commit()

create_caracteristicas_personagem_index_query = "CREATE UNIQUE INDEX id_personagem_UNIQUE ON RPG.caracteristicas_personagem (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_caracteristicas_personagem_index_query)
connection.commit()

# Tabela tipo_dano
drop_tipo_dano_table_query = "DROP TABLE IF EXISTS RPG.tipo_dano;"
with connection.cursor() as cursor:
    cursor.execute(drop_tipo_dano_table_query)
connection.commit()

create_tipo_dano_table_query = """
CREATE TABLE IF NOT EXISTS RPG.tipo_dano (
  id_tipo_dano INT NOT NULL,
  nome_tipo VARCHAR(60) NULL,
  PRIMARY KEY (id_tipo_dano)
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_tipo_dano_table_query)
connection.commit()

# Tabela armas_personagem
drop_armas_personagem_table_query = "DROP TABLE IF EXISTS RPG.armas_personagem;"
with connection.cursor() as cursor:
    cursor.execute(drop_armas_personagem_table_query)
connection.commit()

create_armas_personagem_table_query = """
CREATE TABLE IF NOT EXISTS RPG.armas_personagem (
  id_armas_personagem INT NOT NULL,
  id_personagem INT NOT NULL,
  id_tipo_dano INT NOT NULL,
  nome_arma VARCHAR(45) NULL,
  dado_dano VARCHAR(12) NULL,
  bonus FLOAT NULL,
  extra VARCHAR(120) NULL,
  PRIMARY KEY (id_armas_personagem),
  CONSTRAINT fk_armas_personagem_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_armas_personagem_tipo_dano1 FOREIGN KEY (id_tipo_dano) REFERENCES RPG.tipo_dano (id_tipo_dano) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_armas_personagem_table_query)
connection.commit()

create_armas_personagem_index_query = "CREATE INDEX fk_armas_personagem_personagem1_idx ON RPG.armas_personagem (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_armas_personagem_index_query)
connection.commit()

create_armas_personagem_index_query = "CREATE INDEX fk_armas_personagem_tipo_dano1_idx ON RPG.armas_personagem (id_tipo_dano) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_armas_personagem_index_query)
connection.commit()

# Tabela dinheiro
drop_dinheiro_table_query = "DROP TABLE IF EXISTS RPG.dinheiro;"
with connection.cursor() as cursor:
    cursor.execute(drop_dinheiro_table_query)
connection.commit()

create_dinheiro_table_query = """
CREATE TABLE IF NOT EXISTS RPG.dinheiro (
  id_dinheiro INT NOT NULL,
  id_personagem INT NOT NULL,
  prata FLOAT NULL,
  ouro FLOAT NULL,
  cobre FLOAT NULL,
  platina FLOAT NULL,
  diamante FLOAT NULL,
  PRIMARY KEY (id_dinheiro),
  CONSTRAINT fk_dinheiro_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_dinheiro_table_query)
connection.commit()

create_dinheiro_index_query = "CREATE INDEX fk_dinheiro_personagem1_idx ON RPG.dinheiro (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_dinheiro_index_query)
connection.commit()

create_dinheiro_index_query = "CREATE UNIQUE INDEX id_personagem_UNIQUE ON RPG.dinheiro (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_dinheiro_index_query)
connection.commit()

# Tabela status_base
drop_status_base_table_query = "DROP TABLE IF EXISTS RPG.status_base;"
with connection.cursor() as cursor:
    cursor.execute(drop_status_base_table_query)
connection.commit()

create_status_base_table_query = """
CREATE TABLE IF NOT EXISTS RPG.status_base (
  id_status_base INT NOT NULL,
  id_personagem INT NOT NULL,
  vida INT NULL,
  xp DOUBLE NULL,
  nivel INT NULL,
  alinhamento VARCHAR(45) NULL,
  antecendente VARCHAR(45) NULL,
  faccao VARCHAR(45) NULL,
  inspiracao INT NULL,
  ca INT NULL,
  iniciativa INT NULL,
  deslocamento INT NULL,
  vida_atual INT NULL,
  vida_temporaria INT NULL,
  PRIMARY KEY (id_status_base),
  CONSTRAINT fk_status_base_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_status_base_table_query)
connection.commit()

create_status_base_index_query = "CREATE INDEX fk_status_base_personagem1_idx ON RPG.status_base (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_status_base_index_query)
connection.commit()

create_status_base_index_query = "CREATE UNIQUE INDEX id_personagem_UNIQUE ON RPG.status_base (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_status_base_index_query)
connection.commit()

# Tabela feitico
drop_feitico_table_query = "DROP TABLE IF EXISTS RPG.feitico;"
with connection.cursor() as cursor:
    cursor.execute(drop_feitico_table_query)
connection.commit()

create_feitico_table_query = """
CREATE TABLE IF NOT EXISTS RPG.feitico (
  id_feitico INT NOT NULL,
  id_tipo_dano INT NOT NULL,
  nome_feitico VARCHAR(45) NOT NULL,
  tipo_feitico VARCHAR(15) NOT NULL,
  PRIMARY KEY (id_feitico),
  CONSTRAINT fk_feitico_tipo_dano1 FOREIGN KEY (id_tipo_dano) REFERENCES RPG.tipo_dano (id_tipo_dano) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_feitico_table_query)
connection.commit()

create_feitico_index_query = "CREATE UNIQUE INDEX nome_feitico_UNIQUE ON RPG.feitico (nome_feitico) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_feitico_index_query)
connection.commit()

create_feitico_index_query = "CREATE INDEX fk_feitico_tipo_dano1_idx ON RPG.feitico (id_tipo_dano) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_feitico_index_query)
connection.commit()

# Tabela feitico_personagem
drop_feitico_personagem_table_query = "DROP TABLE IF EXISTS RPG.feitico_personagem;"
with connection.cursor() as cursor:
    cursor.execute(drop_feitico_personagem_table_query)
connection.commit()

create_feitico_personagem_table_query = """
CREATE TABLE IF NOT EXISTS RPG.feitico_personagem (
  id_feitico_personagem INT NOT NULL AUTO_INCREMENT,
  id_feitico INT NOT NULL,
  id_personagem INT NOT NULL,
  PRIMARY KEY (id_feitico_personagem),
  CONSTRAINT fk_feitico_personagem_feitico1 FOREIGN KEY (id_feitico) REFERENCES RPG.feitico (id_feitico) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_feitico_personagem_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_feitico_personagem_table_query)
connection.commit()

create_feitico_personagem_index_query = "CREATE INDEX fk_feitico_personagem_feitico1_idx ON RPG.feitico_personagem (id_feitico) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_feitico_personagem_index_query)
connection.commit()

create_feitico_personagem_index_query = "CREATE INDEX fk_feitico_personagem_personagem1_idx ON RPG.feitico_personagem (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_feitico_personagem_index_query)
connection.commit()

# Tabela salvaguarda
drop_salvaguarda_table_query = "DROP TABLE IF EXISTS RPG.salvaguarda;"
with connection.cursor() as cursor:
    cursor.execute(drop_salvaguarda_table_query)
connection.commit()

create_salvaguarda_table_query = """
CREATE TABLE IF NOT EXISTS RPG.salvaguarda (
  id_salvaguarda INT NOT NULL AUTO_INCREMENT,
  nome_salvaguarda VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_salvaguarda)
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_salvaguarda_table_query)
connection.commit()

create_salvaguarda_index_query = "CREATE UNIQUE INDEX nome_salvaguarda_UNIQUE ON RPG.salvaguarda (nome_salvaguarda) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_salvaguarda_index_query)
connection.commit()

# Tabela salvaguarda_personagem
drop_salvaguarda_personagem_table_query = "DROP TABLE IF EXISTS RPG.salvaguarda_personagem;"
with connection.cursor() as cursor:
    cursor.execute(drop_salvaguarda_personagem_table_query)
connection.commit()

create_salvaguarda_personagem_table_query = """
CREATE TABLE IF NOT EXISTS RPG.salvaguarda_personagem (
  id_salvaguarda_personagem INT NOT NULL AUTO_INCREMENT,
  id_salvaguarda INT NOT NULL,
  id_personagem INT NOT NULL,
  PRIMARY KEY (id_salvaguarda_personagem),
  CONSTRAINT fk_salvaguarda_personagem_salvaguarda1 FOREIGN KEY (id_salvaguarda) REFERENCES RPG.salvaguarda (id_salvaguarda) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_salvaguarda_personagem_personagem1 FOREIGN KEY (id_personagem) REFERENCES RPG.personagem (id_personagem) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
"""
with connection.cursor() as cursor:
    cursor.execute(create_salvaguarda_personagem_table_query)
connection.commit()

create_salvaguarda_personagem_index_query = "CREATE INDEX fk_salvaguarda_personagem_salvaguarda1_idx ON RPG.salvaguarda_personagem (id_salvaguarda) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_salvaguarda_personagem_index_query)
connection.commit()

create_salvaguarda_personagem_index_query = "CREATE INDEX fk_salvaguarda_personagem_personagem1_idx ON RPG.salvaguarda_personagem (id_personagem) USING BTREE;"
with connection.cursor() as cursor:
    cursor.execute(create_salvaguarda_personagem_index_query)
connection.commit()
