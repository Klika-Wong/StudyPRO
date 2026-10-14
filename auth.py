import hashlib
import hmac
import os
import re
import secrets

import mysql.connector


_ITERATIONS = 310_000


def _connect():
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise RuntimeError("Set DB_PASSWORD before connecting to the database.")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=password,
        port=int(os.getenv("DB_PORT", "3306")),
        database="userdetails",
    )


def _derive(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _ITERATIONS
    )


def register_user(user_id, password):
    user_id = user_id.strip()
    if not re.fullmatch(r"[A-Za-z0-9]{1,10}", user_id):
        raise ValueError("User ID must contain 1 to 10 letters or numbers.")
    if len(password) < 10:
        raise ValueError("Password must be at least 10 characters.")

    salt = secrets.token_bytes(16)
    password_hash = _derive(password, salt).hex()
    connection = _connect()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO app_users (user_id, password_salt, password_hash) "
            "VALUES (%s, %s, %s)",
            (user_id, salt.hex(), password_hash),
        )
        connection.commit()
    except mysql.connector.IntegrityError as exc:
        connection.rollback()
        raise ValueError("That user ID is already registered.") from exc
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def authenticate_user(user_id, password):
    user_id = user_id.strip()
    if not user_id or not password:
        return False

    connection = _connect()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT password_salt, password_hash FROM app_users "
            "WHERE user_id = %s",
            (user_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return False
        salt_hex, stored_hash = row
        try:
            salt = bytes.fromhex(salt_hex)
        except (TypeError, ValueError):
            return False
        return hmac.compare_digest(_derive(password, salt).hex(), stored_hash)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
