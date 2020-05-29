import sqlite3

conn = sqlite3.connect('Users.db')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS LoginUsers (
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    User TEXT NOT NULL,
    Password TEXT NOT NULL,
    Cidade TEXT NOT NULL
);
""")
