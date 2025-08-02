import sqlite3

conn = sqlite3.connect("users.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    balance INTEGER DEFAULT 0
)
""")
conn.commit()
conn.close()

print("Database initialized successfully!")
