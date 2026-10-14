import os

import mysql.connector


def _connect(database=None):
    password = os.getenv("DB_PASSWORD")
    user = os.getenv("DB_USER")
    if not password or not user:
        raise RuntimeError("Set DB_USER and DB_PASSWORD before connecting to the database.")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=user,
        password=password,
        port=int(os.getenv("DB_PORT", "3306")),
        database=database or os.getenv("DB_NAME", "questionbank"),
    )


def fetch_records(user_id):
    """Return question history rows for one user."""
    if user_id is None:
        return []

    connection = _connect()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT DISTINCT * FROM questions WHERE user_id = %s",
            (str(user_id),),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def fetch_study_scores(user_id):
    """Return daily correct and total question counts from study_process."""
    if user_id is None:
        return []

    connection = _connect("userdetails")
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT DATE(question_time) AS study_date,
                   SUM(COALESCE(correct_questions, 0)) AS correct_count,
                   SUM(CASE
                       WHEN total_questions > 0 THEN total_questions
                       ELSE COALESCE(correct_questions, 0)
                          + COALESCE(incorrect_questions, 0)
                   END) AS total_count
            FROM study_process
            WHERE user_id = %s
            GROUP BY DATE(question_time)
            ORDER BY study_date
            """,
            (str(user_id),),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()



def record_study_result(user_id, question_id, question_type, is_correct):
    """Save one submitted answer to the user's study history."""
    if user_id is None or question_id is None:
        raise ValueError("A user and question are required.")

    connection = _connect("userdetails")
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO study_process (
                user_id, question_id, question_type,
                correct_questions, incorrect_questions, total_questions
            )
            VALUES (%s, %s, %s, %s, %s, 1)
            """,
            (
                str(user_id),
                int(question_id),
                str(question_type or "Practice"),
                1 if is_correct else 0,
                0 if is_correct else 1,
            ),
        )
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
        raise RuntimeError("Could not save the study result.") from err
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
