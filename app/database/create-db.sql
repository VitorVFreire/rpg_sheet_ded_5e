-- Active: 1686766777179@@127.0.0.1@3306
CREATE DATABASE RPG
    DEFAULT CHARACTER SET = 'utf8mb4';

USE RPG;
drop TABLE user;
CREATE Table user(
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email NVARCHAR(200) NOT NULL UNIQUE,
    password NVARCHAR(200) NOT NULL, 
    datebirth DATE not NULL
);

drop TABLE `character`;
CREATE TABLE `character` (
    id_character INT PRIMARY KEY AUTO_INCREMENT,
    id_user INT NOT NULL,
    FOREIGN KEY (id_user) REFERENCES `user` (id_user),
    class VARCHAR(100) NOT NULL,
    level INT NOT NULL,
    xp INT NOT NULL,
    race VARCHAR(100) NOT NULL,
    background VARCHAR(200),
    alignment VARCHAR(200),
    faction VARCHAR(200)
);

drop TABLE attributes;
CREATE TABLE attributes(
    id_attributes INT PRIMARY KEY AUTO_INCREMENT,
    id_character INT NOT NULL,
    Foreign Key (id_character) REFERENCES `character`(id_character),
    hit_points INT NOT NULL,
    strength INT not NULL,
    dexterity INT NOT NULL,
    constitution INT NOT NULL,
    intelligence INT NOT NULL,
    wisdom INT NOT NULL,
    charisma INT NOT NULL,
    proficiency_bonus INT NOT NULL,
    armor_class INT NOT NULL,
    speed INT,
    initiative INT,
    inspiration INT
);