import sqlite3

DB_NAME = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_or_get_user(username):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user is None:
        conn.execute("INSERT INTO users (username, balance) VALUES (?, ?)", (username, 0))
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def update_balance(user_id, new_balance):
    conn = get_db_connection()
    conn.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = get_db_connection()
    balance = conn.execute("SELECT balance FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return balance["balance"] if balance else 0
