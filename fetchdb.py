import os

import mysql.connector


def _connect(database=None):
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise RuntimeError("Set DB_PASSWORD before connecting to the database.")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
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
