
-- DROP DATABASE IF EXISTS userdetails;

-- 删除 questionbank 数据库
-- DROP DATABASE IF EXISTS questionbank;

-- 创建 userdetails 数据库
CREATE DATABASE userdetails;

-- 切换到 userdetails 数据库
USE userdetails;

-- 创建 user_d 表
CREATE TABLE user_d (
    user_id CHAR(10) PRIMARY KEY,
    user_email VARCHAR(100),
    user_name VARCHAR(20),
    user_password VARCHAR(20)
);

-- 插入示例数据
INSERT INTO user_d (user_id, user_email, user_name, user_password) VALUES 
('1q', 'user102@example.com', '1a', '111'),
('2w', 'user345@example.com', '2b', '222'),
('3e', 'user678@example.com', '3c', '333');

-- drop table study_process;

-- 创建 study_process 表
CREATE TABLE study_process (
    user_id CHAR(10),
    study_notes TEXT
);

-- 创建 questionbank 数据库
CREATE DATABASE questionbank;

-- 切换到 questionbank 数据库
USE questionbank;



drop table questions;

-- 创建 questions 表

CREATE TABLE questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    question_text VARCHAR(100) NOT NULL,  -- 缩短了问题文本的长度
    question_type VARCHAR(50) NOT NULL,   -- 缩短了问题类型的长度
    question_options VARCHAR(100) NOT NULL,  -- 缩短了选项的长度
    correct_answer VARCHAR(50) NOT NULL,  -- 缩短了正确答案的长度
    difficulty_level VARCHAR(20),         -- 缩短了难度级别的长度
    subjects VARCHAR(50) NOT NULL,        -- 缩短了学科的长度
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_called_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id VARCHAR(10)                    -- 缩短了用户ID的长度
);



-- 插入数据
INSERT INTO questions (question_text, question_type, question_options, correct_answer, difficulty_level, subjects, user_id)
VALUES 
('What is the capital of France?', 'Multiple Choice', 'Paris, London, Berlin', 'Paris', '1', 'Geography', '1q'),
('What is 2 + 2?', 'Multiple Choice', '3, 4, 5', '4', '1', 'Mathematics', '1q');



-- 返回到 userdetails 数据库
USE userdetails;

-- 添加外键约束到 study_process 表
-- ALTER TABLE study_process
-- ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES questionbank.questions(question_id);

-- 插入学习过程记录
INSERT INTO study_process (user_id, question_id, qestion_time, qestion_type, correct_questions, incorrect_questions, total_questions, study_notes)
VALUES ('1q', 1, NOW(), 'Multiple Choice', 1, 0, 1, 'Correct answer');



-- ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';

SELECT * FROM user_d;
SELECT * FROM questionbank.questions;
SELECT * FROM study_process;






