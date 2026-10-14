-- Create the databases without replacing existing data.
CREATE DATABASE IF NOT EXISTS userdetails;
CREATE DATABASE IF NOT EXISTS questionbank;

USE userdetails;

CREATE TABLE IF NOT EXISTS user_d (
    user_id CHAR(10) PRIMARY KEY,
    user_email VARCHAR(100),
    user_name VARCHAR(20),
    user_password_hash VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS app_users (
    user_id CHAR(10) PRIMARY KEY,
    password_salt CHAR(32) NOT NULL,
    password_hash CHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

USE questionbank;

CREATE TABLE IF NOT EXISTS questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    question_options TEXT NOT NULL,
    correct_answer VARCHAR(50) NOT NULL,
    difficulty_level VARCHAR(20),
    subjects VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_called_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id VARCHAR(10)
);

USE userdetails;

CREATE TABLE IF NOT EXISTS study_process (
    user_id CHAR(10),
    question_id INT,
    question_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    question_type VARCHAR(50),
    correct_questions INT DEFAULT 0,
    incorrect_questions INT DEFAULT 0,
    total_questions INT DEFAULT 0,
    study_notes TEXT
);
