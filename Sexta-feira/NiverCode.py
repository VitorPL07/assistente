import sqlite3

conectar = sqlite3.connect('Niver.db')

cur = conectar.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS DataNiver (
    Identicicaçao INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    UserNiver TEXT NOT NULL,
    Dia TEXT NOT NULL,
    Mes TEXT NOT NULL
);
""")