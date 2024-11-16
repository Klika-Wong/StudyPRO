import mysql.connector
import json

def insert_question(question_data, user_id, database="questionbank"):
    try:
        # 连接到数据库
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",  # 替换为你的密码
            database=database  # 替换为你的数据库名称
        )
        cursor = connection.cursor()

        # 修改后的 SQL 插入语句，不再包含 call_times
        query = """
        INSERT INTO questions (question_text, question_type, question_options, correct_answer, difficulty_level, subjects, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # 执行插入数据，去掉 call_times 参数
        cursor.execute(query, (
            question_data["question_text"],
            question_data["question_type"],
            json.dumps(question_data["question_options"]),
            question_data["correct_answer"],
            question_data["difficulty_level"],
            question_data["subjects"],
            user_id
        ))

        # 提交事务
        connection.commit()

        # 获取插入的 question_id
        question_id = cursor.lastrowid
        return question_id

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
