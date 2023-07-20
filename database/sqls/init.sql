CREATE DATABASE IF NOT EXISTS mails;

use mails;

CREATE USER IF NOT EXISTS 'local'@'localhost' IDENTIFIED BY 'local';
GRANT ALL PRIVILEGES ON mails.* TO 'local'@'localhost';

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
    sender varchar(255) NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

CREATE TABLE IF NOT EXISTS email_receiver(  
    message_id varchar(25) NOT NULL,
    receiver varchar(255) NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

CREATE TABLE IF NOT EXISTS email_subject(  
    message_id varchar(25) NOT NULL,
    subject varchar(255) NOT NULL,
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

DELIMITER $$
CREATE DEFINER='local'@'localhost' FUNCTION IF NOT EXISTS check_index_exists(
table_name VARCHAR(15), 
column_name VARCHAR(15)
)
RETURNS INTEGER
READS SQL DATA
BEGIN
    DECLARE index_found INT;

    SELECT COUNT(1) INTO index_found
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE table_schema = 'mails'
    AND   table_name   = table_name
    AND   index_name   = column_name;

    RETURN index_found;
END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS create_fti;

DELIMITER $$
CREATE DEFINER='local'@'localhost' PROCEDURE IF NOT EXISTS create_fti()
BEGIN
    IF check_index_exists('email_sender', 'sender') THEN
        ALTER TABLE email_sender ADD FULLTEXT(sender);
    ELSE
        SELECT CONCAT('Index ','sender ','already exists on Table ', 'mails','.','email_sender');   
    END IF;

    IF check_index_exists('email_receiver', 'receiver') THEN
         ALTER TABLE email_receiver ADD FULLTEXT(receiver);
    ELSE
        SELECT CONCAT('Index ','receiver ','already exists on Table ', 'mails','.','email_receiver');   
    END IF;

    IF check_index_exists('email_subject', 'subject') THEN
        ALTER TABLE email_subject ADD FULLTEXT(subject);
    ELSE
        SELECT CONCAT('Index ','subject ','already exists on Table ', 'mails','.','email_subject');   
    END IF;

    IF check_index_exists('email_content', 'content') THEN
        ALTER TABLE email_content ADD FULLTEXT(content);
    ELSE
        SELECT CONCAT('Index ','content ','already exists on Table ', 'mails','.','email_content');   
    END IF;
    
END $$
DELIMITER ;
