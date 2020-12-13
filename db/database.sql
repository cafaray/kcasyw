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
    dsgift VARCHAR(7) NOT NULL,
    dateselection TIMESTAMP NOT NULL,
    datemail TIMESTAMP NULL,
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

DROP TABLE IF EXISTS kmgm99t;
CREATE TABLE kmgm99t (
    iddraw INT NOT NULL,
    startdate DATE NOT NULL,
    enddate DATE NULL,
    access_code VARCHAR(30) NOT NULL,
    tmstmp TIMESTAMP NOT NULL,
    primary key(iddraw),
    foreign key(iddraw)
        REFERENCES kmgm00t(id)
);

-- available gifts
DROP VIEW IF EXISTS kmgv12t;
CREATE VIEW kmgv12t AS 
SELECT dg.iddraw AS iddraw, dg.idgift AS idgift, RIGHT(md5(CONCAT(g.id, g.gift)), 7) alias, g.idgroup As idgroup
  FROM kmgm02t dg INNER JOIN kmgm12t g ON dg.idgift = g.id
 WHERE dg.idgift NOT IN (SELECT idgift FROM kmgm20t WHERE iddraw = dg.iddraw);

-- ******************************************************* --
-- Some useful queries                                     --
-- ******************************************************* --

-- for access an event:
SELECT kmgm01t.iddraw AS kmgm01t_iddraw, kmgm01t.idparticipant AS kmgm01t_idparticipant, kmgm11t.id AS kmgm11t_id, 
        kmgm11t.participant AS kmgm11t_participant, kmgm11t.email AS kmgm11t_email, kmgm11t.idgroup AS kmgm11t_idgroup, 
        kmgm00t.id AS kmgm00t_id, kmgm00t.title AS kmgm00t_title, kmgm00t.fordate AS kmgm00t_fordate, kmgm00t.status AS kmgm00t_status
  FROM kmgm01t INNER JOIN kmgm11t 
    ON kmgm11t.id = kmgm01t.idparticipant INNER JOIN kmgm99t 
    ON kmgm99t.iddraw = kmgm01t.iddraw INNER JOIN kmgm00t 
    ON kmgm00t.id = kmgm01t.iddraw
WHERE kmgm11t.email = %(email_1)s


SELECT dg.iddraw AS iddraw, dg.idgift AS idgift, RIGHT(md5(CONCAT(g.id, g.gift)), 7) alias, g.idgroup As idgroup 
        FROM kmgm02t dg INNER JOIN kmgm12t g 
          ON dg.idgift = g.id 
        WHERE dg.idgift NOT IN 
           (SELECT idgift FROM kmgm20t WHERE iddraw = dg.iddraw)
           AND g.idgroup = 1 AND dg.iddraw = 4 ORDER BY alias;

SELECT * FROM kmgm20t WHERE alias IN('46384be','514cdc7','629534c', '6318577')

SELECT id, gift, description FROM kmgm12t INNER JOIN kmgm02t ON kmgm12t.id = kmgm02t.idgift WHERE kmgm12t.id NOT IN (SELECT idgift FROM kmgm20t WHERE iddraw = 4) AND kmgm02t.iddraw=4;

SELECT A.* FROM kmgm11t A INNER JOIN kmgm01t B ON A.id=B.idparticipant WHERE B.iddraw=4 and A.id NOT IN (SELECT idparticipant FROM kmgm20t WHERE iddraw = 4);