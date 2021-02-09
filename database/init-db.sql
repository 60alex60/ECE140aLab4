CREATE DATABASE IF NOT EXISTS lab4ece140a;

USE lab4ece140a;

-- Create Table here (Ensure it doesn't already exist!)
 CREATE TABLE Commands (
        id integer AUTO_INCREMENT PRIMARY KEY,
        message VARCHAR(32) NOT NULL,
        completed tinyint(1) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);