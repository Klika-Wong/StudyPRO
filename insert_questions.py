import json
import os

import mysql.connector


def _connect(database):
    password = os.getenv("DB_PASSWORD")
    user = os.getenv("DB_USER")
    if not password or not user:
        raise RuntimeError("Set DB_USER and DB_PASSWORD before connecting to the database.")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=user,
        password=password,
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", database),
    )


def insert_question(question_data, user_id, database="questionbank"):
    if user_id is None:
        raise ValueError("A user_id is required.")

    required_fields = {
        "question_text",
        "question_type",
        "question_options",
        "correct_answer",
        "difficulty_level",
        "subjects",
    }
    if not isinstance(question_data, dict) or not required_fields.issubset(question_data):
        raise ValueError("Question data is missing required fields.")
    if not isinstance(question_data["question_options"], dict):
        raise ValueError("question_options must be a JSON object.")

    connection = None
    cursor = None
    try:
        connection = _connect(database)
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO questions (
                question_text, question_type, question_options, correct_answer,
                difficulty_level, subjects, user_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                question_data["question_text"],
                question_data["question_type"],
                json.dumps(question_data["question_options"]),
                question_data["correct_answer"],
                question_data["difficulty_level"],
                question_data["subjects"],
                str(user_id),
            ),
        )
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        if connection is not None:
            connection.rollback()
        raise RuntimeError("Database operation failed.") from err
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
