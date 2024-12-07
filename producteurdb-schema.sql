-- creation du schema de la table message

DROP DATABASE IF EXISTS producteurdb;

CREATE DATABASE producteurdb;

use producteurdb;



CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_ip VARCHAR(255),
    message TEXT,
    dest_ip VARCHAR(255),
    recupere VARCHAR(30) DEFAULT "NON"
);

-- recupere: correspond au statut du paquet : OUI/NON