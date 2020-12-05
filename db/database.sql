-- -------------------------------------------------- --
-- Script for create database project                 --
-- Date: Nov 28, 2020                                 --
-- Created by: cafaray@gmail.com                      --
-- Technology: mysql                                  --
-- -------------------------------------------------- --

DROP DATABASE IF EXISTS kcasyw;
CREATE DATABASE kcasyw CHARACTER SET 'utf8';

use kcasyw;

GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON kcasyw.* TO 'sysadminkcasyw'@'localhost' IDENTIFIED BY 'sV6loU*vS';
FLUSH PRIVILEGES;

-- sorteos
DROP TABLE IF EXISTS kmgm00t;
CREATE TABLE kmgm00t (
    id INT auto_increment,
    title VARCHAR(100) NOT NULL,
    fordate DATE NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'pending',
    primary key(id)
);

-- ALTER TABLE kmgm00t ADD COLUMN status VARCHAR(10) NOT NULL DEFAULT 'pending' AFTER fordate;

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
DROP TABLE IF EXISTS kmgm11t;
CREATE TABLE kmgm11t (
    id INT auto_increment,
    participant VARCHAR(120) NOT NULL,
    email VARCHAR(250) NOT NULL,
    idgroup INT NOT NULL,    
    primary key(id, idgroup),
    foreign key(idgroup)
        REFERENCES kmgm10t(id)
);

-- premios
CREATE TABLE kmgm12t (
    id INT auto_increment,
    gift VARCHAR(200) NOT NULL,
    quantity INT DEFAULT 1,
    description VARCHAR(2000) NOT NULL,
    image TEXT NULL,
    idgroup INT NOT NULL,
    primary key(id, idgroup),
    foreign key(idgroup)
        REFERENCES kmgm10t(id)
);

-- ALTER TABLE kmgm12t ADD COLUMN image TEXT NULL after description;

-- selecciones
DROP TABLE IF EXISTS kmgm20t;
CREATE TABLE kmgm20t (
    id INT auto_increment,
    iddraw INT NOT NULL,
    idparticipant INT NOT NULL,
    idgift INT NOT NULL,    
    dateselection DATE NOT NULL,
    datemail DATE NULL,
    primary key(id, iddraw, idparticipant, idgift),
    foreign key(iddraw)
        REFERENCES kmgm00t(id),
    foreign key(idparticipant)
        REFERENCES kmgm11t(id),
    foreign key(idgift)
        REFERENCES kmgm12t(id)
);

-- selecciones - estados -> obsolote, replaced by fields in the origin table
-- CREATE TABLE kmgm21t (
--     id INT auto_increment,
--     idselection INT NOT NULL,
--     status INT NOT NULL,
--     dateat DATE NOT NULL,
--     primary key(id, idselection),
--     foreign key(idselection)
--         REFERENCES kmgm20t(id)
-- );

-- sorteo-participantes
CREATE TABLE kmgm01t (
    iddraw INT NOT NULL,
    idparticipant INT NOT NULL,
    primary key(iddraw, idparticipant),
    foreign key(iddraw)
        REFERENCES kmgm00t(id),
    foreign key(idparticipant)
        REFERENCES kmgm11t(id)
);

-- sorteo-premios
CREATE TABLE kmgm02t (
    iddraw INT NOT NULL,
    idgift INT NOT NULL,
    primary key(iddraw, idgift),
    foreign key(iddraw)
        REFERENCES kmgm00t(id),
    foreign key(idgift)
        REFERENCES kmgm12t(id)
);