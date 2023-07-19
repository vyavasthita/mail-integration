CREATE DATABASE IF NOT EXISTS mails;

use mails;

CREATE TABLE IF NOT EXISTS label(  
    label_id varchar(25) NOT NULL,  
    name varchar(45) NOT NULL,  
    PRIMARY KEY (label_id)  
);

CREATE TABLE IF NOT EXISTS receiver(  
    id int NOT NULL AUTO_INCREMENT,  
    email varchar(60) NOT NULL,
    PRIMARY KEY (id)  
);

CREATE TABLE IF NOT EXISTS email_message(  
    message_id varchar(25) NOT NULL,
    message varchar(255) NOT NULL,
    receiver int NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (receiver) REFERENCES receiver(id)
);

CREATE TABLE IF NOT EXISTS sender(  
    id int NOT NULL AUTO_INCREMENT,  
    email varchar(60) NOT NULL,
    message varchar(25) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (message) REFERENCES email_message(message_id)
);

CREATE TABLE IF NOT EXISTS subject(  
    id int NOT NULL AUTO_INCREMENT,  
    value varchar(255) NOT NULL,
    message varchar(25) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (message) REFERENCES email_message(message_id)
);

CREATE TABLE IF NOT EXISTS date_info(  
    id int NOT NULL AUTO_INCREMENT,  
    mail_date date NOT NULL,
    message varchar(25) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (message) REFERENCES email_message(message_id)
);
