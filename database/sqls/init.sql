CREATE DATABASE IF NOT EXISTS mails;

use mails;

CREATE TABLE IF NOT EXISTS label(  
    label_id varchar(25) NOT NULL,  
    name varchar(45) NOT NULL,  
    PRIMARY KEY (label_id)  
);

CREATE TABLE IF NOT EXISTS email(  
    message_id varchar(25) NOT NULL,
    is_read BOOLEAN,
    INDEX (is_read),
    PRIMARY KEY (message_id)
);

CREATE TABLE IF NOT EXISTS email_label(
    id int NOT NULL AUTO_INCREMENT,  
    label_id varchar(25) NOT NULL,
    message_id varchar(25) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (label_id) REFERENCES label(label_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

CREATE TABLE IF NOT EXISTS email_sender(  
    message_id varchar(25) NOT NULL,
    sender varchar(50) NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

CREATE TABLE IF NOT EXISTS email_receiver(  
    message_id varchar(25) NOT NULL,
    receiver varchar(50) NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

CREATE TABLE IF NOT EXISTS email_subject(  
    message_id varchar(25) NOT NULL,
    subject varchar(50) NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

CREATE TABLE IF NOT EXISTS email_content(  
    message_id varchar(25) NOT NULL,
    content MEDIUMTEXT NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

CREATE TABLE IF NOT EXISTS email_date(  
    message_id varchar(25) NOT NULL,
    received date NOT NULL,
    PRIMARY KEY (message_id),
    INDEX (received),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

DROP PROCEDURE IF EXISTS create_fti;

DELIMITER $$
CREATE PROCEDURE create_fti()
BEGIN
    ALTER TABLE email_sender ADD FULLTEXT(sender);
    ALTER TABLE email_receiver ADD FULLTEXT(receiver);
    ALTER TABLE email_subject ADD FULLTEXT(subject);
    ALTER TABLE email_content ADD FULLTEXT(content);
    ALTER TABLE email_sender ADD FULLTEXT(sender);
END $$
DELIMITER ;