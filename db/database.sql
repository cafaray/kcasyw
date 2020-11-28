-- -------------------------------------------------- --
-- Script for create database project                 --
-- Date: Nov 28, 2020                                 --
-- Created by: cafaray@gmail.com                      --
-- Technology: mysql                                  --
-- -------------------------------------------------- --

DROP DATABASE IF EXISTS kcasyw;
CREATE DATABASE kcasyw CHARACTER SET 'utf8';

use kcasyw;

-- sorteos
CREATE TABLE kmgm00t (
    id INT auto_increment,
    title VARCHAR(100) NOT NULL,
    fordate DATE NOT NULL,
    primary key(id)
);

CREATE UNIQUE INDEX mgm00_idx_name ON kmgm00t(title);

-- grupos
CREATE TABLE kmgm10t (
    id INT auto_increment,
    groupname VARCHAR(100) NOT NULL,
    description VARCHAR(200) DEFAULT '',
    primary key(id)    
);

CREATE UNIQUE INDEX mgm00_idx_name ON kmgm10t(groupname);

-- participantes
CREATE TABLE kmgm11t (
    id INT auto_increment,
    participant VARCHAR(120) NOT NULL,
    email VARCHAR(250) NOT NULL,
    idgroup INT NULL REFERENCES kmgm10t(id),
    primary key(id)        
);

-- premios
CREATE TABLE kmgm12t (
    id INT auto_increment,
    gift VARCHAR(200) NOT NULL,
    quantity INT DEFAULT 1,
    description VARCHAR(2000) NOT NULL,
    idgroup INT NULL REFERENCES kmgm10t(id),
    primary key(id)        
);

-- selecciones
CREATE TABLE kmgm20t (
    id INT auto_increment,
    iddraw INT NOT NULL,
    idparticipant INT NOT NULL,
    idgitf INT NOT NULL,    
    primary key(id)        
);

-- selecciones - estados
CREATE TABLE kmgm21t (
    id INT auto_increment,
    idselection INT NOT NULL,
    status INT NOT NULL,
    dateat DATE NOT NULL,
    primary key(id, idselection),
    foreign key(idselection)
    REFERENCES kmgm20t(id)
);