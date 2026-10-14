import os

import mysql.connector


def _connect():
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise RuntimeError("Set DB_PASSWORD before connecting to the database.")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=password,
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "questionbank"),
    )


def fetch_records(user_id):
    """Return distinct question rows for one user."""
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
