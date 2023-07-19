CREATE DATABASE IF NOT EXISTS mails;

use mails;

CREATE TABLE IF NOT EXISTS label(  
    label_id varchar(25) NOT NULL,  
    name varchar(45) NOT NULL,  
    PRIMARY KEY (label_id)  
);

CREATE TABLE IF NOT EXISTS User(  
    id int NOT NULL AUTO_INCREMENT,  
    email varchar(60) NOT NULL,  
    PRIMARY KEY (id)  
);

CREATE TABLE IF NOT EXISTS Message(  
    message_id varchar(25) NOT NULL,  
    user int NOT NULL,  
    PRIMARY KEY (message_id),
    FOREIGN KEY (user) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Sender(  
    id int NOT NULL AUTO_INCREMENT,  
    email varchar(60) NOT NULL,
    message varchar(25) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (message) REFERENCES Message(message_id)
);

CREATE TABLE IF NOT EXISTS Subject(  
    id int NOT NULL AUTO_INCREMENT,  
    value varchar(255) NOT NULL,
    message varchar(25) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (message) REFERENCES Message(message_id)
);

CREATE TABLE IF NOT EXISTS DateInfo(  
    id int NOT NULL AUTO_INCREMENT,  
    mail_date date NOT NULL,
    message varchar(25) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (message) REFERENCES Message(message_id)
);
